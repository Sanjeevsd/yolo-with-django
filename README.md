# yolo-with-django
The project uses yolo data model for multi oject detection in realtime using webcam implemented in django webframework.

  The django contains webcamera function which opens webcam and the video is fed to yolo model. The yolo model uses neural network to divide the video into images then to small boundary boxes and predicts the class object. The boundary boxes is then combined with the image and label.All the images are sent to django in form of BYTES, the bytes are automatically converted in video and streamed in new Window of webbrowser.
  ScreenShots:

![GitHub Logo](/screenshots/yolohome.png)
![GitHub Logo](/screenshots/cell1.png)
![GitHub Logo](/screenshots/persons.png)

