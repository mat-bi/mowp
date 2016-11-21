import os

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileSystemModel

from Event import Event
from Track import Track
from mainwindow import *
from Player import Player, Player_Ops, EventManager
from Playlist import Playlist
from PlaylistFile import PlaylistFile

old_volume = 100


class MyListModel(QAbstractItemModel):
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self)
        self.__data = Playlist([])

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return None

        if QModelIndex.row() > len(self.__data):
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return os.path.basename(str(self.__data[QModelIndex.row()]))

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def flags(self, QModelIndex):
        flags = super(MyListModel, self).flags(QModelIndex)
        if QModelIndex.isValid():
            flags |= Qt.ItemIsDragEnabled
        else:
            flags = Qt.ItemIsDropEnabled
        return flags

    def insertRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        self.beginInsertRows(QModelIndex(), p_int, p_int + p_int_1 - 1)
        for _ in range(0, p_int_1):
            self.__data.add_track(Track(None))
        self.endInsertRows()

    def removeRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        self.beginRemoveRows(QModelIndex(), p_int, p_int_1 + p_int - 1)
        for _ in range(0, p_int_1):
            self.__data.remove_track(number=(p_int + _))
        self.endRemoveColumns()
        return True

    def getNodeFromIndex(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return list(self.__data)

    def parent(self, index):
        node = self.getNodeFromIndex(index)
        return self.createIndex(0, 0, 0)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def index(self, row, column, parentIndex):
        parentNode = self.getNodeFromIndex(parentIndex)
        childNode = parentNode[row]
        if childNode:
            newIndex = self.createIndex(row, column, childNode)
            return newIndex
        else:
            return QtCore.QModelIndex()

    def setData(self, QModelIndex, Any, role=None):
        if not QModelIndex.isValid() or role != Qt.EditRole:
            return False

        self.__data.remove_track(number=QModelIndex)
        self.__data.add_track(Any)
        self.__data.track_change_place(len(self.__data) - 1, QModelIndex)
        self.dataChanged.emit(QModelIndex, QModelIndex)
        return True

    def setDataList(self, playlist):
        self.__data = playlist


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
            fileName, _ = QFileDialog.getOpenFileName(self, 'Wczytaj playlistę', '/home',
                                                      filter="Mowp file (*.mowp.xml)")
            playlist = PlaylistFile.open(str(fileName))
            model = MyListModel()
            model.setDataList(playlist)
            ui.playlista.setModel(model)

    widget = Widget()
    widget.showDialog()


def mute_clicked():
    global ui, old_volume
    if Player.get_instance().volume == 0:
        set_volume(old_volume)
        ui.mute.setIcon(QIcon('Grafiki/Speaker-mowp.png'))

    else:
        set_volume(0)
        old_volume = Player.get_instance().volume
        ui.mute.setIcon(QIcon('Grafiki/Mute-mowp.png'))


        # ui.volumeControl.setValue(0)
        # Player.get_instance().volume = 0


def brakRadio_clicked():
    Player.get_instance().playlist_opt = Player_Ops.Normal


def utworRadio_clicked():
    Player.get_instance().playlist_opt = Player_Ops.RepeatTrack


def next_clicked():
    Player.get_instance().increase_time()


def previous_clicked():
    Player.get_instance().decrease_time()


def lista_clicked():
    Player.get_instance().playlist_opt = Player_Ops.RepeatPlaylist


def stop_clicked():
    Player.get_instance().stop_track()


def play_clicked():
    Player.get_instance().play_track()


def ustaw_pauza(args):
    args["user"]["playPause"].setIcon(QIcon("Grafiki/pause.png"))


def ustaw_play(args):
    args["user"]["playPause"].setIcon(QIcon("Grafiki/playArrow.png"))


def ustaw_tytul(args):
    args["user"]["tytul"].setText(args["title"][0])


def random_onclick():
    global ui
    if Player.get_instance().playlist_opt != Player_Ops.RandomTrack:
        ui.random.setIcon(QIcon("Grafiki/shuffleOn.png"))
        Player.get_instance().playlist_opt = Player_Ops.RandomTrack
    else:
        opt = Player_Ops.Normal
        if ui.utworRadio.isChecked():
            opt = Player_Ops.RepeatTrack
        elif ui.listaRadio.isChecked():
            opt = Player_Ops.RepeatPlaylist

        Player.get_instance().playlist_opt = opt
        ui.random.setIcon(QIcon("Grafiki/shuffleOff.png"))


def ustaw_czas_calkowity(args):
    args["user"]["czasCalkowity"].setText("/{}:{}".format(int(args["length"] / 60), int(args["length"] % 60)))

czas_qtimer = QTimer()

def co_sekunde_ustaw_czas(event=None):
    global ui
    czas = Player.get_instance().time
    ui.label.setText("{}:{}".format(int(czas/60), int(czas%60)))

def ustaw_czas(args):
    czas_qtimer = QTimer()
    ui.label.setText("00:00")
    czas_qtimer.setInterval(1)
    czas_qtimer.timeout.connect(co_sekunde_ustaw_czas)
    czas_qtimer.start()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    player = Player.get_instance()

    global ui
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    ui.playPause.clicked.connect(pause)
    ui.volumeControl.valueChanged.connect(value_changed)

    ui.mute.clicked.connect(mute_clicked)
    model = QFileSystemModel()
    ui.wczytaj.clicked.connect(wczytaj_onclick)
    ui.brakRadio.clicked.connect(brakRadio_clicked)
    ui.utworRadio.clicked.connect(utworRadio_clicked)
    ui.random.clicked.connect(random_onclick)
    EventManager.get_instance().add_event(Event.MediaPaused, ustaw_play, {"playPause": ui.playPause})
    EventManager.get_instance().add_event(Event.MediaPlay, ustaw_pauza, {"playPause": ui.playPause})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_play, {"playPause": ui.playPause})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_tytul, {"tytul": ui.label_3})
    EventManager.get_instance().add_event(Event.MediaPlay, ustaw_czas_calkowity, {"czasCalkowity": ui.czasCalkowity})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_czas_calkowity, {"czasCalkowity": ui.czasCalkowity})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_czas)

    ui.next.clicked.connect(next_clicked)
    ui.previous.clicked.connect(previous_clicked)
    ui.listaRadio.clicked.connect(lista_clicked)
    ui.stop.clicked.connect(stop_clicked)

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
    player.current_playlist = Playlist(["/home/mat-bi/tb.mp3", "/home/mat-bi/tb2.mp3"])
    player.play_track()
    sys.exit(app.exec_())
