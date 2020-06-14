import pytesseract
import numpy as np
from cnocr import CnOcr 

from PIL import Image

        

class OCR_tesseract(object):
    """docstring for OCR_tesseract"""
    def __init__(self):
        pass


    def run(self, img):
        content = pytesseract.image_to_string(img, lang='chi_sim')   # 解析图片
        content = content.replace(" ","")
        content = content.replace("\n","")

        return content
        
class OCR_cnocr(object):
    """docstring for OCR_tesseract"""
    def __init__(self):
        self.ocr = CnOcr() 


    def run(self, img):
        nary = np.asarray(img)
        res = self.ocr.ocr(nary)
        
        content = ""
        for r in res:
            for x in r:
                content = content + x
        return content