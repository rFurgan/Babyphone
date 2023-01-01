# Source
# https://gist.github.com/fopina/3cefaed1b2d2d79984ad7894aef39a68

#!/usr/bin/env python

from pyaudio import PyAudio, paInt16
from socket import socket, AF_INET, SOCK_STREAM


class ClientMicrophone:

    ADDR = '127.0.0.1'
    PORT = 8080
    FORMAT = paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 4096

    def __init__(self):
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind((self.ADDR, self.PORT))
        self.__audio = PyAudio()
        self.__stream = self.__audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                          rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)

    def start(self):
        # self.__stream.start_stream()
        while True:
            data = self.__socket.recv(self.CHUNK)
            self.__stream.write(data)

    def stop(self):
        self.__socket.close()
        self.__stream.close()
        self.__audio.terminate()
