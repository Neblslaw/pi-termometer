#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from pydoc import text

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in0g
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)


class Screen:
    def __init__(self):
        self.epd = epd3in0g.EPD()
        self.epd.init()
        self.epd.Clear()
        self.font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    def clear(self):
        self.epd.init()
        self.epd.Clear()

    def exit(self):
        self.epd.Clear()
        self.epd.sleep()

    def draw(self, text):
        self.epd.init()
        Himage = Image.new('RGB', (self.epd.width, self.epd.height), self.epd.BLACK)
        draw = ImageDraw.Draw(Himage)
        draw.text((5, 0), text, font=self.font, fill=self.epd.WHITE)
        self.epd.display(self.epd.getbuffer(Himage))

try:
   screen = Screen()
   screen.draw("hello world")
   time.sleep(30)
   screen.exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in0g.epdconfig.module_exit(cleanup=True)
    exit()
