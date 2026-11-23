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


def draw(text):
    # Drawing on the image
    epd.init()
    Himage = Image.new('RGB', (epd.width, epd.height), epd.BLACK)
    draw = ImageDraw.Draw(Himage)
    draw.text((5, 0), text, font=font24, fill='#9f06a6')
    epd.display(epd.getbuffer(Himage))
    time.sleep(30)

try:
    epd = epd3in0g.EPD()   
    epd.init()
    epd.Clear()
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)

    draw('hello world')


    epd.init()
    logging.info("Clear...")
    epd.Clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in0g.epdconfig.module_exit(cleanup=True)
    exit()
