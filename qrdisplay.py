#!/usr/bin/env python

##
 #  @filename   :   main.cpp
 #  @brief      :   2.9inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 31 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import time
import sys
import epd2in7b
import RPi.GPIO as GPIO
import qrcode
import Image
import ImageFont
import ImageDraw
import textwrap
#import imagedata

COLORED = 1
UNCOLORED = 0

def generate_qr_image(ssid, key):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2
    )
    qr.add_data('WIFI:S:{};T:WPA;P:{};;'.format(ssid, key))
    qr.make()
    return qr.make_image(fill_color="black", back_color="white")


def display_qr_code(ssid, key):
    epd = epd2in7b.EPD()
    epd.init()
    epd.set_rotate(epd2in7b.ROTATE_0)

    # clear the frame buffer
    frame_black = [0] * (epd.width * epd.height / 8)
    frame_red = [0] * (epd.width * epd.height / 8)

    qr_image = generate_qr_image(ssid, key)
    width, height = qr_image.size
    image_padding = max(0, (epd.width - width) // 2)
    epd.draw_image(
            frame_black,
            max(0, (epd.width - width) // 2),
            max(0, (epd.height - height) // 2),
            qr_image
        )

    epd.display_frame(frame_black, frame_red)

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.IMAGE_BLACK, imagedata.IMAGE_RED)
    epd.sleep()
    GPIO.cleanup()

def display_ssid_and_key(ssid, key):
    epd = epd2in7b.EPD()
    epd.init()
    epd.set_rotate(epd2in7b.ROTATE_90)
    
    # clear the frame buffer
    frame_black = [0] * (epd.width * epd.height / 8)
    frame_red = [0] * (epd.width * epd.height / 8)
    
    font_height = 16
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', font_height)
    line_height = font_height + 2
    y = 2
    epd.draw_string_at(frame_black, 2, y, "SSID:", font, COLORED)
    y = y + line_height
    epd.draw_string_at(frame_black, 2, y,"{}".format(ssid), font, COLORED)
    y = y + line_height
    epd.draw_string_at(frame_black, 2, y, "Key:", font, COLORED)
    y = y + line_height
    epd.draw_string_at(frame_black, 2, y, "{}".format(" ".join(textwrap.wrap(key, 4))), font, COLORED)

    epd.display_frame(frame_black, frame_red)

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.IMAGE_BLACK, imagedata.IMAGE_RED)
    epd.sleep()
    GPIO.cleanup()

def wait_for_button_press(t=1000):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    c = GPIO.wait_for_edge(5, GPIO.FALLING, timeout=t)
    GPIO.cleanup()
    return c

def main():
    if len(sys.argv) != 3:
        print("Usage: qrdisplay ssid key")
        sys.exit(1)
    ssid = sys.argv[1]
    key = sys.argv[2]
    while True:
        try:
            display_qr_code(ssid, key)
            while wait_for_button_press() is None:
                pass
            display_ssid_and_key(ssid, key)
            time.sleep(30)
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise
        

if __name__ == '__main__':
    main()
