# Coub Downloader
Forked from [pcroland/coub_likes_downloader](https://github.com/pcroland/coub_likes_downloader)

Download Looped Coubs.

Why fork?
[video here]

# Requirements
- ffmpeg

# Installation

```
git clone https://github.com/uunnxx/coub_downloader && cd coub_downloader
pip install -r requirements.txt
```

# Usage
- Download the `cookies.txt` and put it next to the script using [this expansion](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid), e.g.
- Run the script.

## Examples

```

# First download coub:
python get_coub.py -l                            # download liked videos
python get_coub.py -b                            # download bookmarked videos
python get_coub.py -u username                   # download all coubs of user `username`
python get_coub.py https://coub.com/view/39qnvs  # download coub

- Then:
python coubify.py
```
