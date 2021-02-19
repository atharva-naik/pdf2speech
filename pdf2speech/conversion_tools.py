import os
import random
import tempfile
from colors import color
from string import ascii_letters, digits

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

class PDF2IMG:
    def __init__(self, path):
        self.path = path
        self.rel_path = path.split('/')[-1] 
        self.op_path = None
        self.img_paths = []
        self.images = []
        self.length = 0

    def dump(self, random=False):
        '''
        Dump images in a randomly named folder
        '''
        if random:
            op_path = ''.join(random.sample(ascii_letters+digits+'_', 16))
        else:
            op_path = self.rel_path.replace(".pdf", "")
        
        self.op_path = os.path.join(os.getcwd(), op_path)
        os.mkdir(self.op_path)
        print(color(f"Images saved at {self.op_path} ...", fg='blue', style='bold'))
        
        for i,image in enumerate(convert_from_path(self.path)):
            fname = os.path.join(self.op_path, f"{i}.jpeg")
            self.img_paths.append(fname)
            self.images.append(image)
            image.save(fname)
        self.length = len(self.img_paths)

        return self.op_path

    def __str__(self):
        return f"path set to: {self.path},\noutput will be saved at {self.op_path}.\n{self.length} images detected"

    def __repr__(self):
        return self.__str__()

    def clear(self):
        '''
        Clear the dumped assets. 
        '''
        os.system(f"rm -r {self.op_path}")
        

# def dump_pdf2img(path):
#     '''
#     Dump images in a randomly named folder
#     '''
#     op_path = ''.join(random.sample(ascii_letters+digits+'_', 16))
#     op_path = os.path.join(os.getcwd(), op_path)
#     os.mkdir(op_path)
#     print(color(f"Images saved at {op_path} ...", fg='blue', style='bold'))
#     for i,image in enumerate(convert_from_path(path)):
#         fname = os.path.join(op_path, f"{i}.jpeg")
#         image.save(fname)
    
#     return op_path