# About
`iptv-rec` lets you easily watch and record IPTV channels with CLI. Main feature is [IPTV-Cat](https://iptvcat.com) integration for stream searching.
### Supported OS
- Linux
- Windows
# Configuration
You need to install all requirements.
## Requirements
- [Python 3.x](https://python.org/downloads/)
- [VLC media player](https://videolan.org/vlc)
## Install requirements
To install all requirements on:
- Debian-based systems:
```
sudo apt update && sudo apt install -y python3 vlc
```
- Windows (run in PowerShell with admin privileges):
```
winget install --id=VideoLAN.VLC -e ; winget install --id=Python.Python.3 -e
```
## Modules
Install required Python modules:
```
pip3 install -r requirements.txt
```
## py2exe
If you want, you can build this project with py2exe to use independently from Python interpreter on Windows.
### Install py2exe
Install py2exe Python module:
```
pip3 install py2exe
```
### Setup
```
py .\setup.py py2exe
```
Distributable version will be located in `dist/` folder.
# Usage
### CLI interface
Run help for usage.
- Linux:
```
./iptv-rec.py --help
```
- Windows:
```
py .\iptv-rec.py --help
```