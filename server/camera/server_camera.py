# Source
# https://github.com/ancabilloni/udp_camera_streaming

#!/usr/bin/env python

from cv2 import VideoCapture, imencode, destroyAllWindows
from struct import pack
from math import ceil
from socket import socket, AF_INET, SOCK_DGRAM


class ServerCamera:

    ADDR = '127.0.0.1'
    PORT = 8080
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64  # extract 64 bytes in case UDP frame overflown

    def __init__(self):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__video_capture = VideoCapture(0)

    def start(self):
        while (self.__video_capture.isOpened()):
            _, frame = self.__video_capture.read()
            self.__udp_frame(frame)

    def stop(self):
        self.__video_capture and self.__video_capture.release()
        destroyAllWindows()
        self.__socket.close()

    def __udp_frame(self, img):
        """ 
        Compress image and Break down
        into data segments 
        """
        compress_img = imencode('.jpg', img)[1]
        dat = compress_img.tobytes()
        size = len(dat)
        count = ceil(size/(self.MAX_IMAGE_DGRAM))
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            self.__socket.sendto(pack("B", count) +
                                 dat[array_pos_start:array_pos_end],
                                 (self.ADDR, self.PORT)
                                 )
            array_pos_start = array_pos_end
            count -= 1
