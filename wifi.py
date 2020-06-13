import time
import epd2in7b
import RPi.GPIO as GPIO
import qrcode
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import textwrap
import threading

COLORED = 1
UNCOLORED = 0

def generate_qr_image(ssid, key):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4
    )
    qr.add_data('WIFI:S:{};T:WPA;P:{};;'.format(ssid, key))
    qr.make()
    return qr.make_image(fill_color="black", back_color="white")


def display_qr_code(ssid, key):
    epd = epd2in7b.EPD()
    epd.init()
    epd.set_rotate(epd2in7b.ROTATE_0)
    
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
    epd.sleep()

def display_ssid_and_key(ssid, key):
    epd = epd2in7b.EPD()
    epd.init()
    epd.set_rotate(epd2in7b.ROTATE_90)
    
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

def toggle(ssid, key):
    display_ssid_and_key(ssid, key)
    time.sleep(30)
    display_qr_code(ssid, key)


display_toggle_thread = None

def create_event_callback(ssid, key):
    def event_callback(channel):
        global display_toggle_thread
        if display_toggle_thread is None or not display_toggle_thread.is_alive():
            print("Handling button {} press".format(channel))
            display_toggle_thread = threading.Thread(target = toggle, name = "Display toggle", args=(ssid, key))
            display_toggle_thread.start()
        else:
            print("Already handling {} button press".format(channel))
    return event_callback
