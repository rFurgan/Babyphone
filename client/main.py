from camera.client_camera import *
from microphone.client_microphone import *
from time import sleep

if __name__ == '__main__':
    cm = ClientCamera()
    # cm = ClientMicrophone()
    cm.start()
    sleep(3)
    cm.stop()
