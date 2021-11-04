import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('training_data.npy', allow_pickle=True)

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

forwards = []
lefts = []
backwards = []
rights = []
space = []
left_click = []
right_click = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]
    mouse_pos = data[2]

    if choice == [1, 0, 0, 0, 0, 0, 0]:
        forwards.append([img, choice, mouse_pos])
    elif choice == [0, 1, 0, 0, 0, 0, 0]:
        lefts.append([img, choice, mouse_pos])
    elif choice == [0, 0, 1, 0, 0, 0, 0]:
        backwards.append([img, choice, mouse_pos])
    elif choice == [0, 0, 0, 1, 0, 0, 0]:
        rights.append([img, choice, mouse_pos])
    elif choice == [0, 0, 0, 0, 1, 0, 0]:
        space.append([img, choice, mouse_pos])
    elif choice == [0, 0, 0, 0, 0, 1, 0]:
        left_click.append([img, choice, mouse_pos])
    elif choice == [0, 0, 0, 0, 0, 0, 1]:
        right_click.append([img, choice, mouse_pos])
    else:
        print('no matches')

smallest = 9999999999999999999999999999999

for data in (forwards, lefts, backwards, rights, space, left_click, right_click):
    if len(data) < smallest:
        smallest = len(data)

forwards = forwards[:smallest]
lefts = lefts[:smallest]
backwards = backwards[:smallest]
rights = rights[:smallest]
space = space[:smallest]
left_click = left_click[:smallest]
right_click = right_click[:smallest]

final_data = forwards + lefts + backwards + rights + space + left_click + right_click
shuffle(final_data)

np.save('training_data_v2.npy', final_data, allow_pickle=True)