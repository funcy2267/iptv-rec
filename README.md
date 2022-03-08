# About
`iptv-rec` lets you easily watch and record IPTV channels with CLI and [IPTV-Cat](https://iptvcat.com) integration for stream searching.
# Setup
## Linux
Install requirements (Debain-based systems):
```
sudo apt update && sudo apt install -y python3 python3-pip vlc && pip3 install -r ./requirements.txt
```
Installation:
```
INSTALL_DEST="/usr/local/bin/iptv-rec" && sudo cp ./iptv-rec.py $INSTALL_DEST && sudo chmod +x $INSTALL_DEST
```
### Usage
```
iptv-rec --help
```
## Windows
Install requirements (run in PowerShell with admin privileges):
```
winget install --id=VideoLAN.VLC -e ; winget install --id=Python.Python.3 -e
```
Re-login and run:
```
pip3 install -r .\requirements.txt
```
### Usage
```
py .\iptv-rec.py --help
```
