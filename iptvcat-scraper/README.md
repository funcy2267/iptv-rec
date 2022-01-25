# Configuration
Install required Go modules and build the scraper:
- Linux:
```
go install && go build
```
- Windows (PowerShell):
```
go install ; go build
```
# Usage
- Linux: `./iptvcat-scraper channel_name`
- Windows: `.\iptvcat-scraper.exe channel_name`

Scraped data from IPTV-Cat will be saved to `all-streams.json`.
# Credits
- This is modified version of [eliashussary/iptvcat-scraper](https://github.com/eliashussary/iptvcat-scraper).
