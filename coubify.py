#!/usr/bin/env python3

import os
import subprocess

from pathlib import Path
from rich import print


audio_files = set()
video_files = set()


def list_files():
    # subdir, dirs, files
    for _, dirs, files in os.walk('./temp/', topdown=True):
        del dirs[:]
        for file in files:
            if file.endswith('.mp3'):
                audio_files.add(Path(file).stem)
            elif file.endswith('.mp4'):
                video_files.add(Path(file).stem)

    actual_list = list(audio_files & video_files)

    if actual_list:
        return actual_list

    exit(1)


def join_files(files):
    for file in files:
        file = rename_file(file)
        ffmpeg = (
            f'ffmpeg -stream_loop -1 -i "./temp/{file}.mp4" -c copy -v 0 '
            '-f nut - | ffmpeg -thread_queue_size 100M -i - '
            f'-i "./temp/{file}.mp3" -c copy -map 0:v -map 1:a '
            f'-shortest -y "./output/{file}.mp4"'
        )

        subprocess.run(ffmpeg, shell=True)
        remove_files(file)


def rename_file(file):
    sanitized_filename = file\
            .replace('`', '_')\
            .replace('$', '_')\
            .replace("'", '_')\
            .replace('"', '_')


    os.rename(f"./temp/{file}.mp4", f"./temp/{sanitized_filename}.mp4")
    os.rename(f"./temp/{file}.mp3", f"./temp/{sanitized_filename}.mp3")

    return sanitized_filename


def remove_files(file):
    os.remove(f'./temp/{file}.mp3')
    os.remove(f'./temp/{file}.mp4')
    print(f'Removed {file}.mp3 and {file}.mp4')


def main():
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = list_files()
    join_files(file_list)

    white_delimeter = f"[color(231)]{'-' * os.get_terminal_size()[0]}[/color(231)]"
    print(white_delimeter)
    print(
        '[magenta]Count of unique processed coubs: '
        f'[bold magenta]{len(file_list)}[/bold magenta][/magenta]'
    )
    print(white_delimeter)


if __name__ == '__main__':
    main()
