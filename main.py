from PyQt5.uic.properties import QtWidgets
from mainwindow import *
from Player import Player
from Playlist import Playlist

def pause():
    Player.get_instance().pause_track()

def value_changed(value):
    Player.get_instance().volume = value
    global ui
    if value == 99:
        ui.label_2.setText("100%")
    else:
        ui.label_2.setText("{}%".format(value))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    player = Player.get_instance()
    player.current_playlist = Playlist([])
    player.play_track()
    global ui
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    ui.playPause.clicked.connect(pause)
    ui.volumeControl.valueChanged.connect(value_changed)
    MainWindow.show()
    sys.exit(app.exec_())

