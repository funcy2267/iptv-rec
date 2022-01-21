# About
**iptv-rec** lets you easily watch and record IPTV channels.\
Main feature is IPTV-Cat integration for easy stream searching.
## Support
Supported OS:
- Linux
- Windows
# Requirements
Installed:
- Python 3.x
- GoLang
- VLC
# Configuration
## Dependencies
To install all dependencies on:
- Debian-based systems:
```
sudo apt update && sudo apt install python3 golang vlc -y
```
- Windows systems (run with **admin** privileges):
```
winget install --id=GoLang.Go -e  && winget install --id=VideoLAN.VLC -e  && winget install --id=Python.Python.3 -e
```
## Scraper
- *cd* into `iptvcat-scraper` directory:
```
cd iptvcat-scraper/
```
- Prepare scraper:
```
mkdir data && go install && go build
```
# Usage
Run `./iptv-rec.py` or `py .\iptv-rec.py` with following arguments provided:
- `--name` [required] - channel name to search (use `_` instead of spaces)
- `--mode` [optional] - `r` for **record**, `p` for **preview** (**server** mode is always launched by default, you can use multiple at the same time)
- `--status` [optional] - filter channels by status [**online**/**offline**]
- `--country` [optional] - filter channels by country (use lowercase letters and `_` instead of spaces)
- `--liveliness` [optional] - filter channels by liveliness (higher than `x`%)
- `--mbps`  [optional] - filter channels by Mbps (higher than `x`)
- `--autosort` [optional] - sort channels by [**liveliness**/**mbps**] from highest to smallest and pick the first one automatically (useful in scripts, as it does not ask for anything)
- `--output` [optional] - output file for recording (must be an `.mpg`)
- `--time` [optional] - time limit for recording/preview in *seconds* (the default is **60**)
- `--link` [optional] - use custom link for IPTV stream
- `--target` [optional] - use custom target in VLC server (default is **127.0.0.1**)
- `--port` [optional] - use custom port in VLC server (default is **8989**)