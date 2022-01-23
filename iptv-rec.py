#!/usr/bin/python3
import sys
import os
import subprocess
import platform
import time
import json

args = sys.argv
ScraperPath = './iptvcat-scraper/'
PlatformName = platform.system()

VLC_SERVER_TARGET = "127.0.0.1"
VLC_SERVER_PORT = "8989"

arg_output = 'output.mpg'
arg_timeout = 0
arg_autosort = ''
arg_status = ''
arg_country = ''
arg_liveliness = 0
arg_mbps = 0
arg_mode = 's'
arg_link = ''

i=0
for arg in args:
    if arg == "--name":
        arg_name = args[i+1]
    if arg == "--mode":
        arg_mode = arg_mode + args[i+1]
    if arg == "--status":
        arg_status = args[i+1]
    if arg == "--country":
        arg_country = args[i+1].lower()
    if arg == "--liveliness":
        arg_liveliness = int(args[i+1])
    if arg == "--mbps":
        arg_mbps = int(args[i+1])
    if arg == "--autosort":
        arg_autosort = args[i+1]
    if arg == "--output":
        arg_output = args[i+1]
    if arg == "--timeout":
        arg_timeout = int(args[i+1])
    if arg == "--link":
        arg_link = args[i+1]
    if arg == "--target":
        VLC_SERVER_TARGET = args[i+1]
    if arg == "--port":
        VLC_SERVER_PORT = args[i+1]
    i=i+1

VLC_SERVER_URL = VLC_SERVER_TARGET+':'+VLC_SERVER_PORT

if PlatformName == 'Linux':
    VLC_BIN = 'vlc'
if PlatformName == 'Windows':
    VLC_BIN = os.environ['PROGRAMFILES']+'/VideoLAN/VLC/vlc.exe'

def scrap_data():
    os.chdir(ScraperPath)
    if PlatformName == 'Linux':
        os.system('./iptvcat-scraper '+arg_name)
    if PlatformName == 'Windows':
        os.system('.\\iptvcat-scraper.exe '+arg_name)
    try:
        ScrapedData = json.loads(open('all-streams.json', "r", encoding="utf8").read())
    except:
        print("ERROR: Failed to read stream list.")
        exit()
    os.chdir('..')
    return(ScrapedData)

def select_stream_link(ScrapedData):
    result = []
    for stream in ScrapedData:
        if arg_status in stream['status'] and arg_country in stream['country'] and int(stream['liveliness']) >= arg_liveliness and int(stream['mbps']) >= arg_mbps:
            result = result + [stream]

    if arg_autosort != '':
        hv = 0
        hv_index = 0
        for stream in result:
            if int(stream[arg_autosort]) > hv:
                hv = int(stream[arg_autosort])
                result_index = hv_index
            hv_index = hv_index + 1
    else:
        separator = ' | '
        i=1
        for stream in result:
            print(str(i)+'.', stream['channel']+separator+"Country: "+stream['country']+separator+"Liveliness: "+str(stream['liveliness'])+separator+"Status: "+stream['status']+separator+"Last checked: "+stream['lastChecked']+separator+"Format: "+stream['format']+separator+"mbps: "+str(stream['mbps']))
            i=i+1
        result_index = int(input('Which stream to use? '))-1
    return(result[result_index]['link'])

def vlc_start():
    if 's' in arg_mode:
        VLC_ARGS = ['-I', 'dummy', '-vvv', stream_link, '--sout', '#standard{access=http,mux=ts,dst='+VLC_SERVER_URL+'}', '--sout-all', '--sout-keep', '--repeat']
        global sp_vlc_server
        sp_vlc_server = subprocess.Popen([VLC_BIN] + VLC_ARGS)
        print("VLC server started.")
    if 'r' in arg_mode:
        VLC_ARGS = ['-I', 'dummy', '-vvv', 'http://'+VLC_SERVER_URL, '--sout', '#standard{access=file,mux=ts,dst='+arg_output+'}', '--sout-all']
        if arg_timeout > 0:
            VLC_ARGS = VLC_ARGS + ['--run-time='+str(arg_timeout)]
        global sp_vlc_record
        sp_vlc_record = subprocess.Popen([VLC_BIN] + VLC_ARGS)
        print("VLC recording started.")
    if 'p' in arg_mode:
        VLC_ARGS = ['-vvv', 'http://'+VLC_SERVER_URL]
        if arg_timeout > 0:
            VLC_ARGS = VLC_ARGS + ['--run-time='+str(arg_timeout)]
        global sp_vlc_preview
        sp_vlc_preview = subprocess.Popen([VLC_BIN] + VLC_ARGS)
        print("VLC preview started.")

def vlc_terminate():
    if 's' in arg_mode:
        sp_vlc_server.terminate()
        print("VLC server terminated.")
    if 'r' in arg_mode:
        sp_vlc_record.terminate()
        print("VLC recording terminated.")
    if 'p' in arg_mode:
        sp_vlc_preview.terminate()
        print("VLC preview terminated.")

if arg_link == '':
    stream_link = select_stream_link(scrap_data())
else:
    stream_link = arg_link
vlc_start()

if arg_timeout == 0:
    input("Press enter to quit...")
else:
    time.sleep(arg_timeout)
vlc_terminate()
