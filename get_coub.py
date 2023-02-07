#!/usr/bin/env python3

import http.cookiejar
import subprocess
import requests
import sys

from rich import print
from rich.progress import track


def main():
    search = arg_parse()
    session = requests.Session()
    session.cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
    session.cookies.load()

    pages = get_pages(session, search)
    url_list = prepare_batch(pages, session, search)
    batch_download(url_list)


def arg_parse():
    if len(sys.argv) < 2:
        program_name = sys.argv[0]
        print(
            "[red][bold]ERROR![/bold] Usage:\n[/red]"
            "[magenta]"
            f"[bold]{program_name} likes[/bold]\n"
            f"[bold]{program_name} bookmarks[/bold]\n"
            f"[bold]{program_name} user[/bold] username.\n"
            f"Or just give coub link: "
            f"[bold]{program_name} https://coub.com/view/39qnvs"
            "[/magenta]"
        )
        sys.exit(1)
    else:
        args = sys.argv[1:]
        match args:
            case [coub] if 'coub.com' in coub:
                download_coub(coub)
            case ['likes'] | ['l']:
                search = 'likes'
            case ['bookmarks'] | ['b']:
                search = 'favourites'
            case ['user', user]:
                search = f"channel/{user}"

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
    sys.exit(0)


def get_pages(session, search):
    a = session.get(
        f'https://coub.com/api/v2/timeline/{search}?page=1&per_page=25'
    ).json()

    try:
        pages = a['total_pages']
        print(f'[bold cyan]{pages}[/bold cyan]')
        return pages
    except Exception:
        print(
            '[red][bold]ERROR:[/bold] Incorrect username [bold]'
            f'{search.split("/")[1]}[/bold]?[/red]'
        )
        sys.exit(1)

    print(
        '[color(231)]Fetching number of pages of[/color(231)] '
        f'[magenta]api/v2/timeline/[bold]{search}[/bold][/magenta]: ',
        end=''
    )




def prepare_batch(pages, session, search):
    url_list = []

    for page in track(
            range(1, pages + 1),
            description='[color(231)]Grabbing links... [/color(231)]'
        ):
        page = session.get(
            f'https://coub.com/api/v2/timeline/{search}?page={page}'
            '&per_page=25'
        ).json()

        coubs = page['coubs']
        for coub in coubs:
            url_list.append(coub['permalink'])
    print(
        '[color(231)]Number of coubs:[/color(231)] '
        f'[bold cyan]{len(url_list)}[/bold cyan]'
    )

    return url_list


def batch_download(url_list):
    for url in track(
            url_list,
            description='[color(231)]Grabbing videos...[/color(231)]'):
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
