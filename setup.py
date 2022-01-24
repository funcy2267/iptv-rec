from setuptools import setup
import py2exe
import shutil
import os

setup(console=['iptv-rec.py', 'iptv-rec-gui.py'])

src_scraper = 'iptvcat-scraper/iptvcat-scraper.exe'
dst_scraper = 'dist/iptvcat-scraper/'
os.makedirs(os.path.dirname(dst_scraper), exist_ok=True)
shutil.copy(src_scraper, dst_scraper)
