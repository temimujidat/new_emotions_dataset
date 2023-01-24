import json
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import os
import re
from dotenv import dotenv_values
import requests
import urllib.request


app = Flask(__name__)
s3_url = dotenv_values(".env")['S3_URL']

emotion_array = []

def update_emotion_array():
    global camera_instance, emotion_array
    detected_emotion = camera_instance.process_frame(mode='string')
    emotion_array.append(detected_emotion)
    print(emotion_array)


@app.route('/emotions')

def emotions():
    video_url = request.args.get('campaign_url')
    r = None
    
    try:
        #if url is defined
        if video_url:
            req = urllib.request.Request(video_url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            requests = urllib.request.urlopen(req)
            content_type = requests.getheader('Content-Type')
            
            
        #if url is not defined
        else:
            error_nourl = {'status_code' : 204,
                     'data' : 'null',
                     'message' : "URL is undefined. Input URL"}
            
            #converting to json string
            error_nourl_string = json.dumps(error_nourl, indent = 4)
            
            #write json string to file
            with open ('error_nourl.json', "w") as file:
                file.write(error_nourl_string)
            
            return (error_nourl_string)
            
        
        
    #if url is defined but not valid
    except:
        error_url = {'status_code' : 400,
                 'data' : 'null',
                 'message' : "URL is invalid"}
        
        #converting to json string
        error_url_string = json.dumps(error_url, indent = 4)
        
        #write json string to file
        with open ('error_url.json', "w") as file:
            file.write(error_url_string)
        
        return (error_url_string)
        

        
    #if url is valid and is a video link
    if re.match("video*", content_type):
        
        global camera_instance
        camera_instance = VideoCamera(video_url)
        print('Video is ', camera_instance.video_duration, 'seconds long.')

        print('Processing video..')
        print('fps: ', camera_instance.fps)
        nframes = 0
        while camera_instance.video.isOpened():
            camera_instance.get_frame()
            if camera_instance.frame is None:
                break

            if nframes%camera_instance.fps == 0:
                print('nframes: ', nframes)
                update_emotion_array()

            nframes += 1
            # print('nframes: ', nframes)

        data = {}
        
        for i in range(1,round(camera_instance.video_duration)):

            seconds = i
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            data[":%d:%02d:%02d" % (hour, minutes, seconds)] = emotion_array[i]
        return data
    
    
    #if url is valid but not a video link
    else:
        error_notvideo = {'status_code' : 400,
                 'data' : 'null',
                 'message' : "URL is not a video link"}
        
        #converting to json string
        error_notvideo_string = json.dumps(error_notvideo, indent = 4)
        
        #write json string to file
        with open ('error_notvideo.json', "w") as file:
            file.write(error_notvideo_string)
        
        return (error_notvideo_string)
    
    
    #url = s3_url + str(vid_id) +'.mp4' #Assumes all files are mp4
    
    
    #print('\nVideo url: ', url)
    # return video_url

# def gen(camera):
#     frame = camera.get_frame()
#     yield (b'--frame\r\n'
#            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(camera_instance),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

port = os.environ.get('PORT', 5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
