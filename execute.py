import sys
import vlc
import argparse
from colors import color
from interface import KBHit
from pdf2speech.tts import Engine
from pdf2speech.conversion_tools import PDF2IMG

parser = argparse.ArgumentParser(description='Tool to convert pdfs of books to images')
parser.add_argument('--path', '-p', default=None, help='path of the book to be read')
parser.add_argument('--output', '-o', default='recording.wav', help='path where recording is saved')
args = parser.parse_args()

# PDF2IMG()

if __name__ == '__main__':
    keyboard_controler = KBHit()
             
    # input(color("ENTER to start", bg='yellow', style='bold'))
    eng = Engine() 
    eng.set_io(i='tests/tts.txt', o=args.output)
    eng.speak()
    player = vlc.MediaPlayer(args.output)
    
    # controls for the readout
    print(color(' P', bg='yellow', style='bold')+color(':play/pause', fg='#000', bg='yellow')+color(' ESC', bg='yellow', style='bold')+color(':exit ', fg='#000', bg='yellow'))
    while True:
        try:
            if keyboard_controler.kbhit():
                user_ctrl = keyboard_controler.getch()
                if ord(user_ctrl) == 27:
                    break
                
                elif ord(user_ctrl) in [ord('p'), ord('P')]:
                    if player.is_playing():
                        player.pause()
                    else:
                        player.play() 
        
        except EOFError:
            print("")
            break
        
        except KeyboardInterrupt:
            break

    keyboard_controler.set_normal_term()