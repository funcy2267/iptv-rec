#!/bin/bash
#usage: x.sh http://example.com/playlist.m3u8 output.mpg length_in_sec
#requirements: cvlc

export VLC_DEST="127.0.0.1"
export VLC_PORT="8989"
export VLC_BIN="vlc"

timeout $3s $VLC_BIN -I dummy -vvv $1 --sout "#standard{access=http,mux=ts,dst=$VLC_DEST:$VLC_PORT}" --sout-all --sout-keep --repeat &
timeout $3s $VLC_BIN -I dummy -vvv http://$VLC_DEST:$VLC_PORT --sout "#standard{access=file,mux=ts,dst=$2}" --sout-all --run-time=$3
