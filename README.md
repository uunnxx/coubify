# Coub Downloader
Forked from [pcroland/coub_likes_downloader](https://github.com/pcroland/coub_likes_downloader)

Download Looped Coubs.

Why fork?

[![Watch the video](https://img.youtube.com/vi/nuRaiyjI5lBc/default.jpg)](https://youtu.be/nuRaiyjI5lBc)



## Requirements

```
- ffmpeg
- rich
- yt-dlp
```


## Installation

```
git clone https://github.com/uunnxx/coub_downloader && cd coub_downloader
pip install -r requirements.txt
```


## Usage

- Download the `cookies.txt` and put it next to the script using [this expansion](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid), e.g.
- Run the script.


### Examples

```
# First download coub:
python get_coub.py likes [or just l]             # download liked videos
python get_coub.py bookmarks [or just b]         # download bookmarked videos
python get_coub.py user <username>               # download all coubs of user `username`
python get_coub.py https://coub.com/view/39qnvs  # download coub

# Then:
python coubify.py
```
