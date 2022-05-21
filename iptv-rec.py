#!/usr/bin/python3

import os
import subprocess
import platform
import argparse
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

PlatformName = platform.system()
HTML_PARSER = 'html.parser'
output_ext = ".mpg"

# Parse arguments
parser = argparse.ArgumentParser(description='Search for channel by name or use link and choose mode.')
parser.add_argument('channel_name', help='channel name to search')
parser.add_argument('--link', action="store_true", help='use custom link for IPTV stream instead of channel name')
parser.add_argument('--record', '-r', action="store_true", help='enable recording')
parser.add_argument('--preview', '-p', action="store_true", help='enable preview')
parser.add_argument('--status', default="", help='filter streams by status [online/offline]')
parser.add_argument('--country', default="", help='filter streams by country')
parser.add_argument('--liveliness', type=int, default=0, help='filter streams by liveliness (higher than x percent)')
parser.add_argument('--maturity', type=int, default=0, help='filter streams by maturity (higher than x days)')
parser.add_argument('--mbps', type=int, default=0, help='filter streams by Mbps (higher than x mbps)')
parser.add_argument('--autoselect', '-a', default=False, help='pick stream with the highest value [liveliness/mbps/maturity] from list automatically (no input from user is required)')
parser.add_argument('--output', '-o', default="rec_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+output_ext, help='output file for recording ('+output_ext+')')
parser.add_argument('--timeout', '-t', type=int, default=0, help='timeout for given task in seconds (if not specified, you quit with enter)')
parser.add_argument('--host', default="127.0.0.1", help='use custom host for VLC server')
parser.add_argument('--port', default="8989", help='use custom port for VLC server')
args = parser.parse_args()

arg_channel_name = args.channel_name
arg_mode_server = True
arg_mode_record = args.record
arg_mode_preview = args.preview
arg_timeout = args.timeout
arg_autoselect = args.autoselect
arg_status = args.status
arg_country = args.country
arg_liveliness = args.liveliness
arg_maturity = args.maturity
arg_mbps = args.mbps
arg_output = args.output
arg_stream_link = args.link
VLC_SERVER_HOST = args.host
VLC_SERVER_PORT = args.port
VLC_SERVER_URL = VLC_SERVER_HOST+':'+VLC_SERVER_PORT

# Detect current platform and set binary paths
if PlatformName == "Linux":
    VLC_BIN = "vlc"
if PlatformName == "Windows":
    VLC_BIN = os.environ['PROGRAMFILES']+'/VideoLAN/VLC/vlc.exe'

def format_string(string):
    return(string.replace(" ", "_").lower())

# Scrap and parse data from IPTV-Cat
def scrap_data(search_query):
    headers = {
    	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    	"Accept-Language": "en-US"
    	}
    result = BeautifulSoup(requests.get("https://iptvcat.com/s/"+format_string(search_query), headers=headers).text, HTML_PARSER).prettify().split("\n")
    val_channel_name = []
    val_country = []
    val_link = []
    val_maturity = []
    val_status = []
    val_lastChecked = []
    val_mbps = []
    val_liveliness = []
    val_format = []
    for i in range(len(result)):
        line = result[i]
        if 'span class="channel_name"' in line:
            i2=i
            while "</span>" not in result[i2]:
                i2+=1
            val_channel_name+=[result[i2-1].strip()]
        if 'div class="live green"' in line:
            val_liveliness+=[result[i+1].strip()]
        if 'div class="mature"' in line:
            val_maturity+=[result[i+1].strip()]
        if 'div class="state' in line:
            stream_status = result[i+1].strip()
            if stream_status == "+":
                stream_status_val = "online"
            if stream_status == "-":
                stream_status_val = "offline"
            val_status+=[stream_status_val]
        if 'td class="channel_checked' in line:
            val_lastChecked+=[result[i+2].strip()]
        if 'td class="to_hide"' in line:
            val_format+=[result[i+1].strip()]
        if 'span title=""' in line:
            val_mbps+=[result[i+1].strip()]
        if 'td class="flag"' in line:
            val_country+=[BeautifulSoup(result[i+2].strip(), HTML_PARSER).find()["title"]]
        if 'table class="link_table"' in result[i]:
            val_link+=[BeautifulSoup(result[i+14].strip(), HTML_PARSER).find()["href"]]
    ScrapedData = []
    for i in range(len(val_channel_name)):
    	# Parse channel metadata
        try:
            ScrapedData += [{
            	"channel": val_channel_name[i],
            	"link": val_link[i],
            	"country": val_country[i],
            	"liveliness": val_liveliness[i],
            	"status": val_status[i],
            	"lastChecked": val_lastChecked[i],
            	"format": val_format[i],
            	"mbps": val_mbps[i],
            	"maturity": val_maturity[i]
            }]
        except IndexError:
            # Minimal result parse if data type is unsupported
            try:
            	set_str = "Unknown"
            	set_int = 0
            	ScrapedData += [{
            		"channel": val_channel_name[i]+" [!]",
            		"link": val_link[i],
            		"country": set_str,
            		"liveliness": set_int,
            		"status": set_str,
            		"lastChecked": set_str,
            		"format": set_str,
            		"mbps": set_int,
            		"maturity": set_int
            	}]
            except IndexError:
            	print("Error parsing channel metadata: " + val_channel_name[i])
    return(ScrapedData)

# Interactive stream selection
def select_stream_link(ScrapedData):
    result = []
    for stream in ScrapedData:
        if arg_status in stream["status"] and format_string(arg_country) in format_string(stream["country"]) and int(stream["liveliness"]) >= arg_liveliness and int(stream["maturity"]) >= arg_maturity and int(stream["mbps"]) >= arg_mbps:
            result += [stream]
    if result == []:
        print("No streams found.")
        exit()

    if arg_autoselect == False:
        separator = "\n    "
        i=1
        for stream in result:
            print(str(i)+". "+stream["channel"]+separator+"Country: "+stream["country"]+separator+"Liveliness: "+str(stream["liveliness"])+separator+"Maturity: "+str(stream["maturity"])+separator+"Status: "+stream["status"]+separator+"Last checked: "+stream["lastChecked"]+separator+"Format: "+stream["format"]+separator+"mbps: "+str(stream["mbps"]))
            i+=1
        result_index = int(input("Which stream to use? "))-1
    else:
        highest_value = 0
        i=0
        for stream in result:
            stream_value = int(stream[arg_autoselect])
            if stream_value > highest_value:
                highest_value = stream_value
                result_index = i
            i+=1
    return(result[result_index]["link"])

# Set timeout if defined and start VLC processes
def vlc_start(vlc_stream_link):
    if arg_timeout > 0:
        TIMEOUT_ARG = ['--run-time='+str(arg_timeout)]
    else:
        TIMEOUT_ARG = []
    if arg_mode_server == True:
        VLC_ARGS = ['-I', 'dummy', vlc_stream_link, '--sout', '#standard{access=http,mux=ts,dst='+VLC_SERVER_URL+'}', '--sout-all', '--sout-keep', '--repeat'] + TIMEOUT_ARG
        global sp_vlc_server
        sp_vlc_server = subprocess.Popen([VLC_BIN] + VLC_ARGS)
        print("VLC server started.")
    if arg_mode_record == True:
        VLC_ARGS = ['-I', 'dummy', 'http://'+VLC_SERVER_URL, '--sout', '#standard{access=file,mux=ts,dst='+arg_output+'}', '--sout-all'] + TIMEOUT_ARG
        global sp_vlc_record
        sp_vlc_record = subprocess.Popen([VLC_BIN] + VLC_ARGS)
        print("VLC recording started.")
    if arg_mode_preview == True:
        VLC_ARGS = ['http://'+VLC_SERVER_URL] + TIMEOUT_ARG
        global sp_vlc_preview
        sp_vlc_preview = subprocess.Popen([VLC_BIN] + VLC_ARGS)
        print("VLC preview started.")

# Terminate VLC processes
def vlc_terminate():
    if arg_mode_server == True:
        sp_vlc_server.terminate()
        print("VLC server terminated.")
    if arg_mode_record == True:
        sp_vlc_record.terminate()
        print("VLC recording terminated.")
    if arg_mode_preview == True:
        sp_vlc_preview.terminate()
        print("VLC preview terminated.")

if arg_stream_link == False:
    stream_link = select_stream_link(scrap_data(arg_channel_name))
else:
    stream_link = arg_channel_name
print("Stream: " + stream_link)
print("Target: " + VLC_SERVER_URL)
vlc_start(stream_link)
if arg_timeout != 0:
    time.sleep(arg_timeout)
else:
    input("Press enter to quit...")
vlc_terminate()
