

from PyQt5.QtCore import QDir
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileSystemModel
from mainwindow import *
from Player import Player
from Playlist import Playlist
from PlaylistFile import PlaylistFile

old_volume = 100



def pause():
    Player.get_instance().pause_track()

def set_volume(value):
    global ui
    ui.label_2.setText("{}%".format(value))
    ui.volumeControl.setValue(value)
    Player.get_instance().volume = value

def value_changed(value):
    if value == 99:
        set_volume(100)
    else:
        set_volume(value)

def wczytaj_onclick():
    from PyQt5.QtWidgets import QWidget
    import os
    global ui
    class Widget(QWidget):
        def __init__(self):
            super().__init__()

        def showDialog(self):

            fileName, _ = QFileDialog.getOpenFileName(self, 'Wczytaj playlistę', '/home', filter="Mowp file (*.mowp.xml)")
            playlist = PlaylistFile.open(str(fileName))
            model = QStringListModel()
            playlist2 = []
            for track in playlist:
                playlist2.append(os.path.basename(str(track)))
            model.setStringList(playlist2)
            ui.playlista.setModel(model)


    widget = Widget()
    widget.showDialog()




def mute_clicked():
    global ui, old_volume
    if Player.get_instance().volume == 0:
        ui.mute.setIcon(QIcon('Grafiki/Speaker-mowp.png'))
        set_volume(old_volume)
    else:
        old_volume = Player.get_instance().volume
        ui.mute.setIcon(QIcon('Grafiki/Mute-mowp.png'))
        set_volume(0)

    #ui.volumeControl.setValue(0)
    #Player.get_instance().volume = 0




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    player = Player.get_instance()
    player.current_playlist = Playlist(["/home/mat-bi/tb.mp3", "/home/mat-bi/tb2.mp3"])
    player.play_track()
    global ui
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    ui.playPause.clicked.connect(pause)
    ui.volumeControl.valueChanged.connect(value_changed)

    ui.mute.clicked.connect(mute_clicked)
    model = QFileSystemModel()
    ui.wczytaj.clicked.connect(wczytaj_onclick)

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

