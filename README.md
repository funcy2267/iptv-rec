# About
`iptv-rec` lets you easily watch and record IPTV channels.\
Main feature is IPTV-Cat integration for searching streams.
# Requirements
- python3
- golang
- vlc
# Configuration
Inside `iptvcat-scraper` directory:
- Run `mkdir data && go install && go build` to create *data/* folder, install dependencies and build the scraper.
# Usage
Run `./iptv` with following options:
- `--name` [required] - channel name to search (use `_` instead of spaces)
- `--mode` [required] - `r` for **record**, `p` for **preview** (you can use both at the same time)
- `--status` [optional] - filter channels by status [`online`/`offline`]
- `--country` [optional] - filter channels by country (use lowercase letters)
- `--liveliness` [optional] - filter channels by liveliness (higher than `x`%)
- `--mbps`  [optional] - filter channels by Mbps (higher than `x`)
- `--autosort` [optional] - sort channels by [`liveliness`/`mbps`] from highest to smallest and pick the first one automatically (useful in scripts)
- `--output` [optional] - output file for recording (must be an `.mpg`)
- `--time` [optional] - time limit for recording/preview in *seconds*
