#!/usr/bin/python3
import sys
import os
import subprocess
import platform
import json

VLC_SERVER_DESTINATION = "127.0.0.1"
VLC_SERVER_PORT = "8989"
VLC_SERVER_URL = VLC_SERVER_DESTINATION+':'+VLC_SERVER_PORT

ScraperPath = './iptvcat-scraper/'
args = sys.argv
PlatformName = platform.system()

arg_output = 'output.mpg'
arg_time = 60
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
        arg_country = args[i+1]
    if arg == "--liveliness":
        arg_liveliness = int(args[i+1])
    if arg == "--mbps":
        arg_mbps = int(args[i+1])
    if arg == "--autosort":
        arg_autosort = args[i+1]
    if arg == "--output":
        arg_output = args[i+1]
    if arg == "--time":
        arg_time = int(args[i+1])
    if arg == "--link":
        arg_link = args[i+1]
    i=i+1

if arg_link == '':
    os.chdir(ScraperPath)
    if PlatformName == 'Linux':
        os.system('./iptvcat-scraper '+arg_name)
    if PlatformName == 'Windows':
        os.system('.\\iptvcat-scraper.exe '+arg_name)
    ScrapedData = json.loads(open('data/all-streams.json', "r", encoding="utf8").read())
    os.chdir('..')

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
    stream_link = result[result_index]['link']
else:
    stream_link = arg_link

if PlatformName == 'Linux':
    VLC_BIN = 'vlc'
    CMD_TIMEOUT = 'timeout '+str(arg_time)+'s'
if PlatformName == 'Windows':
    VLC_BIN = os.environ['PROGRAMFILES']+'/VideoLAN/VLC/vlc.exe'
    CMD_TIMEOUT = 'powershell Start-Sleep -S '+str(arg_time)+' ; taskkill /F /IM vlc.exe'

def vlc_start(VLC_ARGS):
    if PlatformName == 'Linux':
        os.system(CMD_TIMEOUT+' '+VLC_BIN+' '+VLC_ARGS+' &')
    if PlatformName == 'Windows':
        subprocess.Popen(VLC_BIN+' '+VLC_ARGS)
        subprocess.Popen(CMD_TIMEOUT)

def vlc_server():
    VLC_ARGS = '-I dummy -vvv '+stream_link+' --sout "#standard{access=http,mux=ts,dst='+VLC_SERVER_URL+'}" --sout-all --sout-keep --repeat'
    vlc_start(VLC_ARGS)
def vlc_record():
    VLC_ARGS = '-I dummy -vvv http://'+VLC_SERVER_URL+' --sout "#standard{access=file,mux=ts,dst='+arg_output+'}" --sout-all --run-time='+str(arg_time)
    vlc_start(VLC_ARGS)
def vlc_preview():
    VLC_ARGS = '-vvv http://'+VLC_SERVER_URL+' --run-time='+str(arg_time)
    vlc_start(VLC_ARGS)

if 's' in arg_mode:
    vlc_server()
if 'r' in arg_mode:
    vlc_record()
if 'p' in arg_mode:
    vlc_preview()
