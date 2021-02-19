import os
import sys
import pyttsx3
import threading 
from threading import Thread

class Engine:
    def __init__(self, volume=1.0, rate=175):
        self.engine=pyttsx3.init()
        self.engine.setProperty('volume', volume)
        self.engine.setProperty('rate', rate)
        self.i = None
        self.o = None
        self.bg_thread = None

    def set_io(self, i=None, o=None):
        if i:
            self.i = open(i, "r")
        if o:
            self.o = o


    def speak(self, text=None):
        if not(text):
            text = self.i.read()
        
        if self.o:
            self.engine.save_to_file(text, self.o)
        else:
            self.engine.say(text)

        self.engine.runAndWait()
        if not(text):
            self.i.close()

    def speak_bg(self, text=None):
        self.bg_thread = Thread(target=self.speak, args=(text,))
        self.bg_thread.daemon = True
        self.bg_thread.start()
    
    def pause(self):
        self.engine.stop()

    def kill(self):
        self.pause()
        self.bg_thread.join()
    # def speak(self, text, clarity=True):
    #     thread = Thread(target=self.say, args=(text,))
    #     thread.daemon = True
    #     thread.start()

    # def say(self, text, clarity=True):
    #     if type(text) == str:
    #         text = [text]
        
    #     for line in text: 
    #         if clarity:
    #             self.say_slowly(line)
    #         else:
    #             self.engine.say(line)
    #         self.engine.runAndWait()

    # def say_slowly(self, text, stride=5):
    #     for word in [(text.split()[i:i+stride]) for i in range(0, len(text.split()), stride)]:
    #         word = ' '.join(word)
    #         self.engine.say(word)
    #         self.engine.runAndWait()