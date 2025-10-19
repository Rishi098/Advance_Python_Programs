import pyautogui as gui
import keyboard
from PIL import Image, ImageGrab
import time
import math

def get_px(img, x, y):
    px = img.load()
    return px[x, y]

def start():
    # Screenshot area
    x, y, w, h = 0, 102, 1920, 872

    # Time variables
    jump_time, last_jump, curr_jump, last_int = 0, 0, 0, 0

    # Search parameters
    y1, y2, x_s, x_e = 557, 486, 400, 415
    y_bird = 460

    # Allow 3s for interface switch
    time.sleep(3)
    while True:
        t1 = time.time()

        # Exit on 'q'
        if keyboard.is_pressed('q'):
            break

        img = gui.screenshot(region=(x, y, w, h))
        img.save("dino.jpg")

        # Get background color
        bg_color = get_px(img, 100, 100)

        # Check for obstacles
        for i in reversed(range(x_s, x_e)):
            if get_px(img, i, y1) != bg_color or get_px(img, i, y2) != bg_color:
                keyboard.press('up')
                jump_time = time.time()
                curr_jump = jump_time
                break
            if get_px(img, i, y_bird) != bg_color:
                keyboard.press("down")
                time.sleep(0.4)
                keyboard.release("down")
                break

        # Adjust for speed
        int_time = curr_jump - last_jump
        if last_int != 0 and math.floor(int_time) != math.floor(last_int):
            x_e += 4
            if x_e >= w:
                x_e = w

        # Update times
        last_jump = jump_time
        last_int = int_time

start()
