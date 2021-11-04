import cv2
import numpy as np
import time
import win32api as wapi
import os
import mouse
from grab_screen import grab_screen

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'APS$/\\":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


def keys_to_output(keys):
    output = [0, 0, 0, 0, 0, 0, 0] #W,A,S,D,<SPACE>,<LEFT CLICK>,<RIGHT CLICK>

    if 'W' in keys:
        output[0] = 1
    elif 'A' in keys:
        output[1] = 1
    elif 'S' in keys:
        output[2] = 1
    elif 'D' in keys:
        output[3] = 1
    elif ' ' in keys:
        output[4] = 1
    elif mouse.is_pressed('left'):
        output[5] = 1
    elif mouse.is_pressed('right'):
        output[6] = 1
    return output


last_time = time.time()

file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('File does not exist, starting fresh!')
    training_data = []

while True:
    screen = grab_screen(region=(0, 40, 1280, 1024))
    mouse_pos = mouse.get_position()
    keys = key_check()
    output = keys_to_output(keys)
    training_data.append([screen, output, mouse_pos])
    #cv2.imshow('window', screen)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    if len(training_data) % 500 == 0:
        print(len(training_data))
        np.save(file_name, training_data, allow_pickle=True)
