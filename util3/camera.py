from picamera.array import PiRGBArray
from picamera import PiCamera

class camera:
    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (640, 480)
        self.rawCapture = PiRGBArray(self.camera)
 
    def capture(self):
        # grab an image from the camera
        self.camera.capture(self.rawCapture, format="bgr")
        return self.rawCapture.array
    
    def trunc(self):
        # truncate the stream
        self.rawCapture.truncate(0)

    def exit(self):
        self.camera.close()
