import cv2
import numpy as np
from django.shortcuts import render

def getCameraId():  #my os gives random video ids to wencams on every boot, tesaile loop lagayera check garya, idk whats alternative
    for i in range(0, 10):
        vd=cv2.VideoCapture(i)
        if vd.isOpened():
            return i
class VideoCamera(object):
    def __init__(self):
        id=getCameraId()
        self.video = cv2.VideoCapture(id)

    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        net = cv2.dnn.readNet('yolov3-tiny.weights', 'yolov3-tiny.cfg')
        classes = []
        with open('coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        cap = self.video
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                img = frame
                height, width, n_channels = img.shape
                blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)
                class_ids = []
                boxes = []
                confidences = []
                for out in outs:
                    for det in out:
                        scores = det[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]

                        if confidence > 0.5:
                            cx = int(det[0] * width)
                            cy = int(det[1] * height)

                            w = int(det[2] * width)
                            h = int(det[3] * height)

                            x = int(cx - w / 2)
                            y = int(cy - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                n_det = len(boxes)
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)  # removes boxes those are alike
                font = cv2.FONT_HERSHEY_PLAIN
                for i in range(n_det):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        label = str(classes[class_ids[i]])
                        color = colors[i]
                        cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
                        cv2.putText(img, label, (x, y + 30), font, 1, color, 3)
                rets, jpegs = cv2.imencode('.jpg', img)
                return jpegs.tobytes()
            else:
                break
        cap.release()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def check():
    print('checking')


def index(request):
    print("sanjeev")
    return render(request,'index.html')