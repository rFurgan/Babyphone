from camera.server_camera import *
from microphone.server_microphone import *
from time import sleep

if __name__ == '__main__':
    sm = ServerCamera()
    # sm = ServerMicrophone()
    sm.start()
    sleep(3)
    sm.stop()
