import random
from colors import color
from colr import Colr as C
BANNER='''
██████╗ ██████╗ ███████╗██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝╚════██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║
██████╔╝██║  ██║█████╗   █████╔╝███████╗██████╔╝█████╗  █████╗  ██║     ███████║
██╔═══╝ ██║  ██║██╔══╝  ██╔═══╝ ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║     ██╔══██║
██║     ██████╔╝██║     ███████╗███████║██║     ███████╗███████╗╚██████╗██║  ██║
╚═╝     ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝     ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝
                                                                                                                                  
'''

import os
import math
# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:
    '''
    A Python class implementing KBHIT, the standard keyboard-interrupt poller.
    Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
    with IDLE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    '''
    def __init__(self):
        '''
        Creates a KBHit object that you can call to do various keyboard things.
        '''
        if os.name == 'nt':
            pass
        
        else:
    
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
    
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    
            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)
    
    
    def set_normal_term(self):
        ''' 
        Resets to normal terminal.  On Windows this is a no-op.
        '''
        if os.name == 'nt':
            pass
        
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' 
        Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        '''
        s = ''
        
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        
        else:
            return sys.stdin.read(1)
                        

    def getarrow(self):
        ''' 
        Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''
        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]
            
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        
        return vals.index(ord(c.decode('utf-8')))
        

    def kbhit(self):
        ''' 
        Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []
    
def rainbow(text):
    res = []
    u,j ='|<82><88><8E>jF"#$%^_^Y^S7[^?~}',0
    for i in text:
        res.append('\x1b[38;5;{}m{}'.format(ord(u[(j*12)//len(text.replace(" ", ""))]), i))
        j+=i!=" "
    
    return ''.join(res)

def _rainbow_rgb(freq, i):
    """ Calculate a single rgb value for a piece of a rainbow.
        Arguments:
            freq  : "Tightness" of colors (see self.rainbow())
            i     : Index of character in string to colorize.
    """
    # Borrowed from lolcat, translated from ruby.
    red = math.sin(freq * i + 0) * 127 + 128
    green = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
    blue = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
    
    return int(red), int(green), int(blue)

def _rainbow_rgb_chars(s, freq=0.1, spread=3.0, offset=0):
    """ 
    Iterate over characters in a string to build data needed for a
    rainbow effect.
    Yields tuples of (char, (r, g, b)).
    Arguments:
        s      : String to colorize.
        freq   : Frequency/"tightness" of colors in the rainbow.
                 Best results when in the range 0.0-1.0.
                 Default: 0.1
        spread : Spread/width of colors.
                 Default: 3.0
        offset : Offset for start of rainbow.
                 Default: 0
    """
    return ((c, _rainbow_rgb(freq, offset + i/spread)) for i, c in enumerate(s))

def rainbow_text(text, spread=2, freq=0.1, offset=0, bg=False, fg=(255,255,255), style=[], rand=False):
    res = ''
    if rand:
        offset = random.randint(0,10)*10

    for (l, (r,g,b)) in _rainbow_rgb_chars(text, spread=spread, freq=freq, offset=offset):
        if bg:
            char = C().b_rgb(r, g, b).rgb(fg[0], fg[1], fg[2], l)
            for sty in style:
                char = color(char, style=sty)
            res += char
        else:
            char = C().rgb(r, g, b, l)
            for sty in style:
                char = color(char, style=sty)
            res += char 

    return res
# Test    
# if __name__ == "__main__":
    
#     kb = KBHit()

#     print('Hit any key, or ESC to exit')

#     while True:

#         if kb.kbhit():
#             c = kb.getch()
#             if ord(c) == 27: # ESC
#                 break
#             print(c)
             
#     kb.set_normal_term()

        
