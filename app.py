from flask import Flask, render_template, Response, redirect, url_for
import cv2
import mediapipe as mp
from math import hypot
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google.protobuf.json_format import MessageToDict
import screen_brightness_control as sbc

app = Flask(__name__)

# Initialize MediaPipe and Pycaw
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75)
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]

# Video feed generator
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            left_lmList, right_lmList = [], []
            if results.multi_hand_landmarks and results.multi_handedness:
                for i in results.multi_handedness:
                    label = MessageToDict(i)['classification'][0]['label']
                    if label == 'Left':
                        for lm in results.multi_hand_landmarks[0].landmark:
                            h, w, _ = img.shape
                            left_lmList.append([int(lm.x * w), int(lm.y * h)])
                        mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)
                    if label == 'Right':
                        index = 0
                        if len(results.multi_hand_landmarks) == 2:
                            index = 1
                        for lm in results.multi_hand_landmarks[index].landmark:
                            h, w, _ = img.shape
                            right_lmList.append([int(lm.x * w), int(lm.y * h)])
                        mpDraw.draw_landmarks(img, results.multi_hand_landmarks[index], mpHands.HAND_CONNECTIONS)

            if left_lmList:
                x1, y1 = left_lmList[4][0], left_lmList[4][1]
                x2, y2 = left_lmList[8][0], left_lmList[8][1]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                length = hypot(x2 - x1, y2 - y1)
                bright = np.interp(length, [15, 200], [0, 100])
                sbc.set_brightness(int(bright))

            if right_lmList:
                x1, y1 = right_lmList[4][0], right_lmList[4][1]
                x2, y2 = right_lmList[8][0], right_lmList[8][1]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                length = hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [15, 200], [volMin, volMax])
                volume.SetMasterVolumeLevel(vol, None)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/main')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
