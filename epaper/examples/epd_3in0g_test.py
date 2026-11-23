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
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()

    def draw(self, data):
        self.epd.init()
        # Swap dimensions to draw along the 400px axis
        width, height = self.epd.height, self.epd.width

        Himage = Image.new('RGB', (width, height), self.epd.WHITE)
        draw = ImageDraw.Draw(Himage)

        rows = [
            ("eCO2", f"{data['eCO2']} ppm"),
            ("TVOC", f"{data['TVOC']} ppb"),
            ("Temp", f"{data['temp']:.1f} °C"),
            ("Humidity", f"{data['humidity']:.1f} %"),
        ]

        margin = 6
        row_height = (height - 2 * margin) // len(rows)
        table_top = margin
        table_bottom = table_top + row_height * len(rows)
        table_left = margin
        table_right = width - margin
        col_split = int(width * 0.45)

        draw.rectangle([(table_left, table_top), (table_right, table_bottom)], outline=self.epd.BLACK, width=2)
        draw.line([(col_split, table_top), (col_split, table_bottom)], fill=self.epd.BLACK, width=2)

        for idx, (label, value) in enumerate(rows):
            y_top = table_top + idx * row_height
            if idx > 0:
                draw.line([(table_left, y_top), (table_right, y_top)], fill=self.epd.BLACK, width=1)

            bbox = draw.textbbox((0, 0), label, font=self.font)
            text_height = bbox[3] - bbox[1]
            text_y = y_top + (row_height - text_height) // 2 - bbox[1]

            draw.text((table_left + 10, text_y), label, font=self.font, fill=self.epd.BLACK)
            draw.text((col_split + 10, text_y), value, font=self.font, fill=self.epd.BLACK)

        # Rotate back to native 168x400 (use 270 instead of 90 if upside-down)
        Himage = Himage.rotate(90, expand=True)

        self.epd.display(self.epd.getbuffer(Himage))
        self.epd.sleep()

try:
   screen = Screen()
   data = {
       "eCO2": 1000,
       "TVOC": 1234,
       "temp": 15,
       "humidity": 97
   }
   screen.draw(data)

   time.sleep(30)
   screen.exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in0g.epdconfig.module_exit(cleanup=True)
    exit()
