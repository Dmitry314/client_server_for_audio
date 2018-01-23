#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:31:51 2018

@author: dmitriy






    First we need to install portaudio module

    sudo apt-get install libasound-dev

    Download portaudio from http://portaudio.com/download.html

    tar -zxvf [portaudio.tgz]

    Enter the directory, ./configure && make

    sudo make install

    sudo pip install pyaudio

    Check the version of pyaudio, it should be 0.2.9

"""

import pyaudio
import wave
 
import socket
import time


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file2.wav"

class recorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
         
        # start Recording
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
       


    def record(self):
        print "recording..."
        self.frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        print "finished recording"
 
 
# stop Recording
    def stop_and_write(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
         
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

    def encrypt(self, data):
        return data #to_do


    def record_and_send(self):
        
        sock = socket.socket()
        sock.connect(('localhost', 9100))
        
        
        print "recording and sending"
        self.frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK)
            sock.send(data)
            
        print "finished recording"
        

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def begin_work_and_wait(self):
        #we have to add multithreading
        sock = socket.socket()
        sock.bind(('', 9101))
        sock.listen(1)
        
        conn, addr = sock.accept()

        print 'connected:', addr
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK)
            sock.send(data)


        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
                      


my_recorder = recorder()
my_recorder.begin_work_and_wait()

