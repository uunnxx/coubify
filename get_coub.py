#!/usr/bin/env python3

import http.cookiejar
import subprocess
import requests
import sys

from rich import print
from rich.progress import track


def main():
    search = parse_args()
    session = requests.Session()
    session.cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
    session.cookies.load()

    pages = get_pages(session, search)
    url_list = prepare_batch(pages, session, search)
    batch_download(url_list)


def parse_args():
    args = [i for i in sys.argv[1:]]

    if len(args) == 0:
        print('[red][bold]ERROR:[/bold] you have to use the -l or -u option or -b.[/red]')
        exit(1)

    elif len(args) == 1:
        value = args[0]
        if 'coub.com' in value:
            download_coub(value)

        elif '-l' in value:
            search = 'likes'
        elif '-b' in value:
            search = 'favourites'
    elif len(args) == 2:
        username = args[1]
        if '-u' in value:
            search = f'channel/{username}'
    return search


def run_cmd(cmd):
    subprocess.run(
        cmd,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )


def download_coub(link):
    yt_dlp = [
        'yt-dlp',
        '-o', './temp/%(title)s_[%(uploader)s] [%(id)s].%(ext)s',
        '-f', 'html5-video-higher, html5-audio-high',
        '-k',
        f'{link}'
    ]
    run_cmd(yt_dlp)
    exit(0)


def get_pages(session, search):
    print('[color(231)]Fetching number of pages of[/color(231)] [magenta]api/v2/timeline/[bold]{search}[/bold][/magenta]: ', end='')

    a = session.get(f'https://coub.com/api/v2/timeline/{search}?page=1&per_page=25').json()
    pages = a['total_pages']
    print(f'[bold cyan]{pages}[/bold cyan]')

    return pages


def prepare_batch(pages, session, search):
    url_list = []

    for page in track(range(1, pages + 1), description='[color(231)]Grabbing links... [/color(231)]'):
        page = session.get(f'https://coub.com/api/v2/timeline/{search}?page={page}&per_page=25').json()
        coubs = page['coubs']
        for coub in coubs:
            url_list.append(coub['permalink'])
    print(f'[color(231)]Number of coubs:[/color(231)] [bold cyan]{len(url_list)}[/bold cyan]')

    return url_list


def batch_download(url_list):
    for url in track(url_list, description='[color(231)]Grabbing videos...[/color(231)]'):
        yt_dlp = [
            'yt-dlp',
            '-o', './temp/%(title)s_[%(uploader)s] [%(id)s].%(ext)s',
            '-f', 'html5-video-higher, html5-audio-high',
            '-k',
            f'https://coub.com/view/{url}'
        ]

        run_cmd(yt_dlp)

    return 0


if __name__ == '__main__':
    main()
