import cv2
from ultralytics import YOLO
import librosa
import sounddevice as sd
wavsignal, rt = librosa.load(r"B:\codes\ds\DLearn\pydlearn\dcam4\alarm.mp3")

model = YOLO(r"B:\codes\ds\DLearn\runs\classify\train30\weights\best.pt")  # load an official model

capture = cv2.VideoCapture(1)
while True:
    ret, frame = capture.read()
    # frame = cv2.flip(frame,1) #镜像操作

    results = model.predict(frame, stream=True)  # predict on an image

    for result in results:
        index = int(result.probs.argmax(-1))
        print(result.names[index], float(result.probs[index]))
        if result.names[index] == 'sleep':
            sd.play(wavsignal, samplerate=rt, blocking=True)

    cv2.imshow("video", frame)
    key = cv2.waitKey(500)
    #print(key)
    if key == ord('q'): #判断是哪一个键按下
        break
cv2.destroyAllWindows()