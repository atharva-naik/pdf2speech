import os
import sys
import vlc
# import tqdm
import gtts
import time
import colour
import argparse
import tempfile
from colors import color
from pdf2speech.tts import Engine
from pdf2speech.ocr import image2text
from interface import KBHit, apply_gradient
from pdf2speech.conversion_tools import PDF2IMG

parser = argparse.ArgumentParser(description='Tool to convert pdfs of books to images')
parser.add_argument('--path', '-p', default=None, help='path of the book to be read')
parser.add_argument('--output', '-o', default=None, help='path where recording is saved')
args = parser.parse_args()

SKIP_DELTA = 5000

if args.path:
    converter = PDF2IMG(args.path)
    img_path = converter.dump()
    # except FileExistsError:
    #     print("This folder already exists. Was this created by pdf2speech?")
    #     if input("If you believe the folder has the recordings, press ENTER to continue: ").strip() == "":
    
else:
    exit("No pdf or jpg supplied!")

def get_formatted_duration(millis):
    millis = int(millis)
    seconds = int((millis/1000)%60)
    minutes = int((millis/(1000*60))%60)
    hours = int((millis/(1000*60*60))%24)

    stamp = str(hours).rjust(2,'0')
    stamp += ':'+str(minutes).rjust(2,'0')
    stamp += ':'+str(seconds).rjust(2,'0')
    # stamp += ':'+str(millis%1000).rjust(3,'0')

    return stamp#("%d:%d:%d    " % (hours, minutes, seconds))

if __name__ == '__main__':
    keyboard_controler = KBHit()

    eng = Engine()          

    current_index = 0
    current_image = os.path.join(img_path, f"{current_index}.jpeg")
    current_recording = os.path.join(img_path, f"{current_index}.mp3")
    
    while True:
        try:

            current_stream = eng.dump_to(image2text(current_image), current_recording)
            #gtts.gTTS(image2text(current_image), lang='en').save(current_recording)
            break
        except FileNotFoundError:
            time.sleep(0.5)
    
    # for file in os.listdir(img_path):
    #     eng.set_io(i=file, o=output_dir)
    #     eng.speak()
    player = vlc.MediaPlayer(current_stream)
    print(f"On page {current_index+1}/{converter.length}".ljust(os.get_terminal_size().columns))
    # controls for the readout
    print(color(' P', bg='yellow', style='bold')+color(':play/pause', fg='#000', bg='yellow')+color(' ESC', bg='yellow', style='bold')+color(':exit ', fg='#000', bg='yellow'))
    while True:
        try:
            percent_completion = player.get_time()/(1e-12+player.get_length())
            pbar_length = max(os.get_terminal_size().columns-22,0)
            pbar = f"{str(int(100 * percent_completion)).rjust(3)}%"
            pbar += apply_gradient("█"*int(percent_completion * pbar_length), ["#FF0000","#00FF00"])
            pbar += " "*(pbar_length - int(percent_completion*pbar_length))
            
            if player.get_length() == -1:
                pbar = " "*pbar_length 

            print(get_formatted_duration(max(player.get_length(),0))+'/'+get_formatted_duration(max(player.get_time(),0))+' '+pbar, end="\r")
        
            if keyboard_controler.kbhit():
                user_ctrl = keyboard_controler.getch()
                if ord(user_ctrl) == 27:
                    print(" "*(os.get_terminal_size().columns), end="\r")
                    break
                
                elif user_ctrl in ['p','P']:
                    if player.is_playing():
                        player.pause()
                    else:
                        player.play() 

                elif user_ctrl in ['r','R']:
                    player.set_time(0)

                elif user_ctrl in ['j','J']:
                    player.set_time(max(player.get_time()-SKIP_DELTA,0))
                
                elif user_ctrl in ['l','L']:
                    player.set_time(min(player.get_time()+SKIP_DELTA, player.get_length()))

                elif user_ctrl in ['d','D']:
                    current_index += 1
                    current_index = min(current_index, converter.length)
                    print(f"On page {current_index+1}/{converter.length}".ljust(os.get_terminal_size().columns))
                    current_image = os.path.join(img_path, f"{current_index}.jpeg")
                    current_recording = os.path.join(img_path, f"{current_index}.mp3")
                    
                    while True:
                        print("d pressed")
                        try:
                            current_stream = eng.dump_to(image2text(current_image), current_recording)
                            print(current_stream)
                            break
                        except FileNotFoundError:
                            time.sleep(0.5)
                    player = vlc.MediaPlayer(current_stream)

                elif user_ctrl in ['a','A']:
                    current_index -= 1
                    current_index = max(current_index, 0)
                    print(f"On page {current_index+1}/{converter.length}".ljust(os.get_terminal_size().columns))
                    current_image = os.path.join(img_path, f"{current_index}.jpeg")
                    current_recording = os.path.join(img_path, f"{current_index}.mp3")

                    while True:
                        try:
                            current_stream = eng.dump_to(image2text(current_image), current_recording)
                            print(current_stream)
                            break
                        except FileNotFoundError:
                            time.sleep(0.5)
                    player = vlc.MediaPlayer(current_stream)

        except EOFError:
        #     print("")
            break
        
        except KeyboardInterrupt:
            break

    keyboard_controler.set_normal_term()