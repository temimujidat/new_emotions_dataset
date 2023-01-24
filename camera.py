import cv2
from model import FacialExpressionModel
import numpy as np

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self, url):
        print('Downloading video..')
        self.video = cv2.VideoCapture(url)
        print('Done.')

        # calculate duration of the video
        frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = fps = int(self.video.get(cv2.CAP_PROP_FPS))
        self.video_duration = frames / fps

    def __del__(self):
        self.video.release()

    #Obtain frame from video capture device
    def get_frame(self):
        _, fr = self.video.read()
        self.frame = fr
        # _, jpeg = cv2.imencode('.jpg', fr)
        # return jpeg.tobytes()

    #Process obtained video frame
    # mode = 'img' returns camera frames along with bounding boxes and predictions.
    # mode = 'string' returns string contatining detected emotion.
    def process_frame(self, mode):
        pred = None
        gray_fr = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            if mode == 'img':
                cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
                cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

        if mode == 'img':
            _, jpeg = cv2.imencode('.jpg', fr)
            return jpeg.tobytes()

        elif mode == 'string':
            if pred == None:
                return 'null'
            else:
                return pred
