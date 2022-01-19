#!/bin/bash
#usage: ---.sh http://example.com/playlist.m3u8 output.mpg time mode
#requirements: vlc

export VLC_SERVER_DEST="127.0.0.1"
export VLC_SERVER_PORT="8989"
export VLC_BIN="vlc"

vlc_server() {
	timeout $3s $VLC_BIN -I dummy -vvv $1 --sout "#standard{access=http,mux=ts,dst=$VLC_SERVER_DEST:$VLC_SERVER_PORT}" --sout-all --sout-keep --repeat
}
vlc_record() {
	timeout $3s $VLC_BIN -I dummy -vvv http://$VLC_SERVER_DEST:$VLC_SERVER_PORT --sout "#standard{access=file,mux=ts,dst=$2}" --sout-all --run-time=$3
}
vlc_preview() {
	timeout $3s $VLC_BIN -vvv http://$VLC_SERVER_DEST:$VLC_SERVER_PORT --run-time=$3
}

vlc_server $1 $2 $3 $4 &
if [[ $4 =~ 'r' ]]; then
	vlc_record $1 $2 $3 $4 &
fi
if [[ $4 =~ 'p' ]]; then
	vlc_preview $1 $2 $3 $4 &
fi