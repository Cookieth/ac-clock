import pytube
import json
import os
import sys
import signal
import shutil
import subprocess
import time
from datetime import datetime

# Honestly kind of confused how this fixes it, but this allows for the killing of the subprocess spawned from the child
def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)

# ===== json parsing portion =====

if not os.path.isfile("./video_logs.json"):
    shutil.copyfile("./video_logs_default.json", "./video_logs.json")

# open json file
with open('video_logs.json','r') as video_logs_json:
    video_logs = json.load(video_logs_json)

# update paths, ensure all videos are downloaded
for video in video_logs["video_urls_paths"]:
    if video_logs["video_urls_paths"][video][1] == "" or not os.path.isfile(video_logs["video_urls_paths"][video][1]):
        print("Video not downloaded, downloading video for hour %s..." % video)
        url = video_logs["video_urls_paths"][video][0]
        yt_video = pytube.YouTube(url)
        print("    Title : %s" % yt_video.title)
        # get the mp4 stream
        path = yt_video.streams.filter(only_audio=True, file_extension='mp4').first().download()
        # log that the video has been downloaded
        video_logs["video_urls_paths"][video][1] = path

if video_logs["bells"][1] == "" or not os.path.isfile(video_logs["bells"][1]):
    print("Bells not downloaded, downloading bells...")
    url = video_logs["bells"][0]
    yt_video = pytube.YouTube(url)
    path = yt_video.streams.filter(only_audio=True, file_extension='mp4').first().download()
    video_logs["bells"][1] = path

# update json file
with open('video_logs.json','w') as video_logs_json:
    json.dump(video_logs, video_logs_json)

# ===== audio playing portion =====

while True:
    hour = datetime.now().hour
    hour_key = str(int(hour / 10)) + str(int(hour % 10))
    # print("Playing hour %s..." % hour_key)

    pid = os.fork()
    # parent process
    if pid > 0 :
        print("Spawned child process:", pid)
        # Get the number of seconds until the next hour
        target_minutes = 60 - datetime.now().minute
        target_seconds = 60 - datetime.now().second  + (target_minutes * 60)
        time.sleep(target_seconds)

        # Kill the subprocess, play the bell sound
        os.kill(pid, signal.SIGTERM)
        os.system("afplay " + "\"" + video_logs["bells"][1] + "\"")
    # child process
    else:
        signal.signal(signal.SIGTERM, sigterm_handler)
        
        while True:
            subp = subprocess.run("afplay " + "\"" + video_logs["video_urls_paths"][hour_key][1] + "\"",\
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# # This works... but only once
# # Spawn a subprocess to play the music, so we can kill it when the bell sound comes up
# subp = subprocess.Popen("afplay " + "\"" + video_logs["video_urls_paths"][hour_key][1] + "\"",\
#             shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# print("    Child process spawned: %d" % subp.pid)
# # Get the number of seconds until the next hour
# # target_hour = max(min(hour + 1, 24), 0)
# target_minutes = 60 - datetime.now().minute
# target_seconds = 3 # 60 - datetime.now().second  + (target_minutes * 60)
# print("Sleeping for %d seconds" % target_seconds)
# time.sleep(target_seconds)
# # Kill the subprocess, play the bell sound
# # os.killpg(os.getpgid(subp.pid), signal.SIGTERM)
# # os.kill(subp.pid, signal.SIGTERM)
# subp.kill()
# print("Playing bells...")
# print(video_logs["bells"][1])
# code = os.system("afplay " + "\"" + video_logs["bells"][1] + "\"")

# old:
# Loop to run everything
# print("    filename: \"%s\"" % video_logs["video_urls_paths"][hour_key][1])
# subprocess.run(['afplay', "\"" + video_logs["video_urls_paths"][hour_key][1] + "\""])
# code = os.system("afplay " + "\"" + video_logs["video_urls_paths"][hour_key][1] + "\"")
# if code == signal.SIGINT:
#     print("Stopping...")
#     exit(0)
