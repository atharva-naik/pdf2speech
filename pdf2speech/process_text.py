import re
import nltk
import emoji
from threading import Thread

PUNCTUATIONS = '''!()-[]{};:'"\, <>./?@#$%^&*_~''' 
# filters
def lower(text):    
    return text.lower()

def upper(text):
    return text.upper()

def unpunct(text):
    for letter in text:
        if letter in PUNCTUATIONS:
            text = text.replace(letter, "")
    
    return text

def remoji(text):
    return emoji.emojize(text)

def unemoji(text):
    return emoji.demojize(text)

def unspace(text):
    return ' '.join(text.split())

def squash(text):
    return ' '.join(text.split('\n'))

def strip(text):
    return text.strip()

def eye(text):
    return text
# filter map (map functions to names)
FILTER_MAP = {'lower':lower, 
              'upper':upper, 
              'unpunct':unpunct, 
              'unemoji':unemoji, 
              'remoji':remoji, 
              'unspace':unspace, 
              'squash':squash, 
              'strip':strip, 
              'eye':eye}

class Clean:
    '''
    Class to pipeline several processing steps, like the Sequential
    model in tensorflow.
    '''
    def __init__(self, filters=[]):
        self.filters = filters
        for filt in self.filters:
            self.add(filt)

    def add(self, filt):
        self.filters.append(filt)

    def run(self, text):
        for filt in self.filters:
            text = FILTER_MAP[filt](text)

        return text 