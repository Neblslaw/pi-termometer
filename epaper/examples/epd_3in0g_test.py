#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in0g
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd3in0g.EPD()   
    epd.init()
    epd.Clear()
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    # Drawing on the image
    epd.init()
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
    draw = ImageDraw.Draw(Himage)
    draw.text((5, 0), 'hello world', font = font24, fill = epd.RED)
    epd.display(epd.getbuffer(Himage))
    time.sleep(30)


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
