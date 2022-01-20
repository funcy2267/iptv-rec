# About
**iptv-rec** lets you easily watch and record IPTV channels.\
Main feature is IPTV-Cat integration for searching streams.
# Requirements
- python3
- golang
- vlc
# Configuration
## Dependencies
To install all dependencies on Debian based systems:
```
sudo apt update && sudo apt install python3 golang vlc -y
```
## Scraper
- *cd* into `iptvcat-scraper` directory:
```
cd iptvcat-scraper
```
- Prepare scraper:
```
mkdir data && go install && go build
```
# Usage
Run `./iptv.py` with following options:
- `--name` [required] - channel name to search (use `_` instead of spaces)
- `--mode` [optional] - `r` for **record**, `p` for **preview** (**server** mode is always launched by default, you can use multiple at the same time)
- `--status` [optional] - filter channels by status [**online**/**offline**]
- `--country` [optional] - filter channels by country (use lowercase letters)
- `--liveliness` [optional] - filter channels by liveliness (higher than `x`%)
- `--mbps`  [optional] - filter channels by Mbps (higher than `x`)
- `--autosort` [optional] - sort channels by [**liveliness**/**mbps**] from highest to smallest and pick the first one automatically (useful in scripts, as it does not ask for anything)
- `--output` [optional] - output file for recording (must be an `.mpg`)
- `--time` [optional] - time limit for recording/preview in *seconds* (the default is **60**)
