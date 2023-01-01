# Source
# https://gist.github.com/fopina/3cefaed1b2d2d79984ad7894aef39a68

#!/usr/bin/env python

import pyaudio
# import select
from socket import socket, AF_INET, SOCK_STREAM


class ServerMicrophone:

    ADDR = '127.0.0.1'
    PORT = 1234
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 4096

    def __init__(self):
        self.__audio = pyaudio.PyAudio()
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind((self.ADDR, self.PORT))
        self.__stream = self.__audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                          input=True, frames_per_buffer=self.CHUNK, stream_callback=self.__callback)

    def __callback(self, in_data, frame_count, time_info, status):
        self.__socket.sendto(in_data, (self.ADDR, self.PORT))
        return (None, pyaudio.paContinue)

    def start(self):
        pass
        # self.__stream.start_stream()
        # while True:
        #     readable, writable, errored = select.select(read_list, [], [])
        #     for s in readable:
        #         if s is serversocket:
        #             (clientsocket, address) = serversocket.accept()
        #             read_list.append(clientsocket)
        #             print("Connection from", address)
        #         else:
        #     data = self.__socket.recv(1024)
        #     print(data)

    def stop(self):
        self.__socket.close()
        self.__stream.stop_stream()
        self.__stream.close()
        self.__audio.terminate()
