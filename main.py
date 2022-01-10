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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VeryMusically')

        uic.loadUi(os.path.abspath('data/creators_space.ui'), self)
        self.spin_octave.setMinimum(2)
        self.spin_octave.setMaximum(6)
        self.sourcefile = ""
        self.data = []
        self.initUI()

    def initUI(self):
        need_opener = False
        while not gen_functions.name_checker(self.sourcefile):
            self.sourcefile, ok_pressed = QInputDialog.getText(self, "Имя нового файла", "Как назовём шедевр?")
            if not ok_pressed:
                while not ok_pressed:
                    self.sourcefile, ok_pressed = QFileDialog.getOpenFileName()
                need_opener = True
                break
                # open an existing file
        if not need_opener:
            self.sourcefile = os.path.abspath('creations/scripts/' + self.sourcefile + '.csv')
        else:
            self.sourcefile = os.path.abspath(self.sourcefile)
        self.opener()

        [i.clicked.connect(self.setter) for i in self.tunesGroup.buttons()]
        self.pb_play_tune.clicked.connect(self.play_note)
        self.pb_open.clicked.connect(self.opener)
        self.pb_play.clicked.connect(self.my_player)
        self.pb_save.clicked.connect(self.saver)

    def my_player(self):
        filename = self.saver()
        self.load_mp3(filename)

    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        self.pb_pause.clicked.connect(self.player.pause)
        self.pb_stop.clicked.connect(self.player.stop)

    def play_note(self):
        if self.ib_scilence.isChecked():
            pass  # *sound of scilence*
        else:
            p1 = self.line_note.text().strip().capitalize()
            p2 = self.spin_octave.value()
            filename = os.path.abspath('data/sounds/guitar/guitar_' + p1 + str(p2) + '.mp3')
            if os.path.isfile(filename):
                # play sound
                self.load_mp3(filename)
            else:
                # TO DO exception no such sound or parameters are incorrect
                pass

    def setter(self):
        pos = int(self.sender().objectName()[-3:])
        if self.ib_scilence.isChecked():
            # set sound
            self.sender().setText('-')
            self.data[pos] = ['S', -1]
            gen_functions.write_update(self.sourcefile, self.data)
        else:
            p1 = self.line_note.text().strip().capitalize()
            p2 = self.spin_octave.value()
            filename = os.path.abspath('data/sounds/guitar/guitar_' + p1 + str(p2) + '.mp3')
            if os.path.isfile(filename):
                # set sound
                self.sender().setText(p1 + str(p2))
                self.data[pos] = [p1, p2]
                gen_functions.write_update(self.sourcefile, self.data)
            else:
                # TO DO exception no such sound or parameters are incorrect
                pass

    def saver(self):
        outfile = self.sourcefile.split('\\')
        outfile[-2] = 'audio'
        outfile[-1] = outfile[-1][:-3] + 'mp3'
        outfile = os.path.abspath('/'.join(outfile))
        sound = AudioSegment.silent(duration=10)
        sound.export(outfile, format="mp3")
        for pos in range(128):
            if self.data[pos][0] == 'S':
                gen_functions.sound_joiner(outfile)
            else:
                adf = os.path.abspath(
                    'data/sounds/guitar/guitar_' + self.data[pos][0] + str(self.data[pos][1]) + '.mp3')
                gen_functions.sound_joiner(outfile, adf)
        return outfile

    def opener(self):
        if os.path.isfile(self.sourcefile):
            self.data = gen_functions.csv_reader(self.sourcefile)
            # loand data
        else:
            for i in range(128):
                self.data.append(['S', -1])
            gen_functions.csv_writer(self.sourcefile, self.data)
            # create file with empty song and create data

        for i in self.tunesGroup.buttons():
            pos = int(i.objectName()[-3:])
            if self.data[pos][0] == 'S':
                i.setText('-')
            else:
                i.setText(self.data[pos][0] + str(self.data[pos][1]))
        # set everything to workspace


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
