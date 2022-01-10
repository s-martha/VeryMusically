import gen_functions
import sys
import os.path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMainWindow, QInputDialog, QWidget
from random import randint
from PyQt5 import QtCore, QtMultimedia
from pydub import AudioSegment
import csv
from pydub.utils import make_chunks


def sound_joiner(main_file, addition_file=''):
    sound1 = AudioSegment.from_file(main_file, format='mp3')
    sound2 = AudioSegment.silent(duration=1000)
    if addition_file != '':
        sound2 = AudioSegment.from_mp3(addition_file)
    sound = sound1 + sound2
    sound.export(main_file, format="mp3")


def csv_reader(filename):
    data = []
    with open(filename, encoding="utf8") as infile:
        reader = csv.DictReader(infile, delimiter=';', quotechar='"')
        for cur in reader:
            data.append([cur['note'], int(cur['octave'])])
    return data


def csv_writer(filename, data):
    with open(filename, 'w', newline='', encoding="utf8") as outfile:
        writer = csv.writer(
            outfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['note', 'octave'])
        for line in data:
            writer.writerow(line)


def write_update(filename, data):
    with open(filename, 'w') as f:
        f.truncate()
    csv_writer(filename, data)


def name_checker(s):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']
    alf1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', ' q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
    alf2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
    symb = ['_', ' '] + numbers + alf1 + alf2
    if len(s) < 3:
        return False
    for i in s:
        if i not in symb:
            return False
    return True
