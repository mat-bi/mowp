

from PyQt5.QtCore import QDir
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel
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


class QStringList(object):
    pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    player = Player.get_instance()
    player.current_playlist = Playlist([])
    #player.play_track()
    global ui
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    ui.playPause.clicked.connect(pause)
    ui.volumeControl.valueChanged.connect(value_changed)
    model = QFileSystemModel()


    model.setRootPath(QDir.currentPath())
    model.sort(0)
    model.setNameFilters(["*.mp3", ".ogg"])
    model.setNameFilterDisables(False)
    ui.treeView.setModel(model)
    ui.treeView.hideColumn(1)
    ui.treeView.hideColumn(2)
    ui.treeView.hideColumn(3)
    ui.treeView.hideColumn(4)

    MainWindow.show()
    sys.exit(app.exec_())

