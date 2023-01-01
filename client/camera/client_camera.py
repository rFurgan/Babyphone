# Source
# https://github.com/ancabilloni/udp_camera_streaming

#!/usr/bin/env python

from cv2 import imdecode, imshow, waitKey, destroyAllWindows
from numpy import fromstring, uint8
from struct import unpack
from socket import socket, AF_INET, SOCK_DGRAM


class ClientCamera:

    ADDR = '127.0.0.1'
    PORT = 8080
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64  # extract 64 bytes in case UDP frame overflown

    def __init__(self):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.bind((self.ADDR, self.PORT))

    def start(self):
        """ Getting image udp frame &
        concate before decode and output image """

        dat = b''
        self.__dump_buffer()

        while True:
            seg, _ = self.__socket.recvfrom(self.MAX_DGRAM)
            if unpack("B", seg[0:1])[0] > 1:
                dat += seg[1:]
            else:
                dat += seg[1:]
                img = imdecode(fromstring(dat, dtype=uint8), 1)
                imshow('frame', img)
                if waitKey(1) & 0xFF == ord('q'):
                    break
                dat = b''

    def stop(self):
        destroyAllWindows()
        self.__socket.close()

    def __dump_buffer(self):
        """ Emptying buffer frame """
        while True:
            seg, _ = self.__socket.recvfrom(self.MAX_DGRAM)
            print(seg[0])
            if unpack("B", seg[0:1])[0] == 1:
                print("finish emptying buffer")
                break
