import pytube
import json
import os

with open('video_logs.json','r') as video_logs_json:
    video_logs = json.load(video_logs_json)

for video in video_logs["video_urls_paths"]:
    if video_logs["video_urls_paths"][video][1] == "" or not os.path.isfile(video_logs["video_urls_paths"][video][1]):
        print("Video not downloaded, downloading video for hour %s..." % video)
        url = video_logs["video_urls_paths"][video][0]
        yt_video = pytube.YouTube(url)
        print("    Title : %s" % yt_video.title)

        # get the mp4 stream
        path = yt_video.streams.filter(file_extension='mp4').first().download()
        # log that the video has been downloaded
        video_logs["video_urls_paths"][video][1] = path

# update json file
with open('video_logs.json','w') as video_logs_json:
    json.dump(video_logs, video_logs_json)



# pytube.YouTube('https://www.youtube.com/watch?v=qDnrdeNDRio').streams.first().download()