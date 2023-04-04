#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:38:35 2023

@author: mac
"""

import os
import boto3
from pathlib import PurePath
import cv2




aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")


s3 = boto3.resource(
    service_name='s3',
    region_name = "us-east-1",
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key =aws_secret_access_key
)

saved_video_dir = r'/Users/mac/Desktop/top'


sentienta_video = s3.Bucket('adsift-files')
for file in sentienta_video.objects.filter(Prefix= "videos/"):
    if file.key.endswith('.webm'):
        local_file_name = os.path.join(saved_video_dir, file.key.split("/")[1])
        print(f"Downloading {file.key} to {local_file_name}")
        sentienta_video.download_file(file.key, local_file_name)
        print(f"Finished downloading {local_file_name}")


#creating image frames from videos
# files = os.listdir(saved_video_dir)
# for file in files:
#     path = os.path.join(saved_video_dir,file)
#     print(path)
#     cam = cv2.VideoCapture(path)

#     try:
#         if not os.path.exists('image'):
#             os.makedirs('image')
#     except OSError:
#         print("error")

#     currentframe = 0
#     while(True):
#         ret,frame = cam.read()

#         if ret:
#             name = './image/frame' +str(currentframe) + file[:8] + ".jpg"
#             print('creating' + name)
#             cv2.imwrite(name,frame)

#             currentframe+=1

#         else:
#             break

#cam = cv2.VideoCapture("tem.mp4")










