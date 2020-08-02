import os
from pytube import Playlist, YouTube
import re
import random


def progress_func(self, chunk=None, bytes_remaining=None, file_handle=None):
    percent = (100 * (file_size - bytes_remaining)) / file_size
    print("{:00.0f}% downloaded".format(percent))


def file_path():
    home = os.path.expanduser("~")
    # Create random names for each download folder to avoid existing directories creation
    new_folder = "Downloads/youtube_videos_%s" % str(random.randint(0, 1000))
    download_folder = os.path.join(home, new_folder)
    access_rights = 0o755
    try:
        os.mkdir(download_folder, access_rights)
    except OSError:
        print("Creation of the directory %s failed" % download_folder)
    else:
        print("Successfully created the directory %s" % download_folder)
    return download_folder


def download_video(url=None, playlist_url=None):
    path = file_path()
    global file_size
    if url:
        yt_fetch = YouTube(url, on_progress_callback=progress_func)
        yt_video = yt_fetch.streams.filter(progressive=True, file_extension="mp4").order_by("resolution")[-1]
        file_size = yt_video.filesize
        yt_video.download(output_path=path)
        print("Video downloaded succesfully")
    elif playlist_url:
        playlist = Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        amount_of_videos = len(playlist.video_urls)
        print("Number of videos in playlist: %s" % amount_of_videos)
        for video, number in zip(playlist, range(0, amount_of_videos)):
            yt_fetch = YouTube(video, on_progress_callback=progress_func)
            numbered_title = str(number + 1) + ") " + yt_fetch.title
            yt_video = yt_fetch.streams.filter(progressive=True, file_extension="mp4").order_by("resolution")[-1]
            file_size = yt_video.filesize
            yt_video.download(filename=numbered_title, output_path=path)
            print("Video #{} downloaded".format(number))


choice = input("Do you want to download a video or a playlist? v/p ")
if str(choice) == "v":
    url = input("Enter the link of the video: ")
    download_video(url=url)
elif str(choice) == "p":
    playlist_url = input("Enter the link of the playlist: ")
    download_video(playlist_url=playlist_url)
