# About
`iptv-rec` lets you easily watch and record IPTV channels. Main feature is [IPTV-Cat](https://iptvcat.com) integration for easy stream searching.
### Supported OS
- Linux
- Windows
# Configuration
You need to [install all requirements](#install-requirements) and [build the scraper](#scraper).
## Requirements
- [Python 3.x](https://python.org/downloads/)
- [GoLang](https://go.dev/dl/)
- [VLC media player](https://videolan.org/)
## Install requirements
To install all requirements on:
- Debian-based systems:
```
sudo apt update && sudo apt install python3 golang vlc -y
```
- Windows (run in PowerShell with admin privileges):
```
winget install --id=VideoLAN.VLC -e ; winget install --id=Python.Python.3 -e ; winget install --id=GoLang.Go -e
```
## Scraper
Go to iptvcat-scraper/ directory and [configure the scraper](iptvcat-scraper/README.md#configuration).
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
Distributable version will be located in dist/ folder.
# Usage
### CLI interface
Run `./iptv-rec.py` (Linux) or `py .\iptv-rec.py` (Windows) with following arguments provided:
- `--name` - channel name to search (use `_` instead of spaces)
- `--mode` - `r` for **record**, `p` for **preview** (**server** mode is always launched by default, you can use multiple at the same time)
- `--status` - filter channels by status [**online**/**offline**]
- `--country` - filter channels by country (use `_` instead of spaces)
- `--liveliness` - filter channels by liveliness (higher than `x`%)
- `--mbps` - filter channels by Mbps (higher than `x`)
- `--autosort` - sort channels by [**liveliness**/**mbps**] from highest to smallest and pick the first one automatically (useful in scripts, as it does not ask for anything)
- `--output` - output file for recording (must be an `.mpg` file, use `_` instead of spaces)
- `--timeout` - timeout for given task in *seconds* (if not specified, you quit with enter)
- `--link` - use custom link for IPTV stream
- `--target` - use custom target in VLC server (default is **127.0.0.1**)
- `--port` - use custom port in VLC server (default is **8989**)
### GUI interface
Run `./iptv-rec-gui.py` (Linux) or `py .\iptv-rec-gui.py` (Windows).
