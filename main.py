import os

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QMessageBox

from Event import Event
from Track import Track
from mainwindow import *
from Player import Player, Player_Ops, EventManager
from Playlist import Playlist
from PlaylistFile import PlaylistFile

old_volume = 100

'''
class MyListModel(QAbstractListModel):
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self)
        self.__data = Playlist([])

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return None

        return QVariant(str(self.__data[QModelIndex.row()]))

    def setDataList(self, playlist):
        self.__data = playlist
        self.beginInsertRows(self.createIndex(0,len(self.__data)-1),0,len(self.__data)-1)
        self.endInsertRows()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)



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
'''

def ciemny_click():
    global ui, MainWindow
    ui.jasny.setIcon(QIcon("Grafiki/Motyw-off.png"))
    ui.ciemny.setIcon(QIcon("Grafiki/Motyw-on.png"))
    ui.treeView.setStyleSheet("* {background-color: #000A23;}")
    ui.playlista.setStyleSheet("* {background-color: #000A23}")

    MainWindow.setStyleSheet("* {background-color: #000A23;} QMainWindow {  color: #00BBFF;} QPushButton { background-color: #000A23}; Line {background-color: #000A23};")


def jasny_click():
    global ui, MainWindow
    ui.jasny.setIcon(QIcon("Grafiki/Motyw-on.png"))
    ui.ciemny.setIcon(QIcon("Grafiki/Motyw-off.png"))
    ui.treeView.setStyleSheet("* {background-color: #FFFFFB; color: #00BBFF;}")
    ui.playlista.setStyleSheet("* {background-color: #FFFFFB}")
    MainWindow.setStyleSheet("QMainWindow { background-color: #FFFFFB; color: #00BBFF;} #treeView { background-color: #FFFFFB} #playlista { background-color: #FFFFFB }")
    #palette.setColorGroup()


def pause():
    Player.get_instance().pause_track()


def set_volume(value):
    global ui
    ui.label_2.setText("{}%".format(value))
    ui.volumeControl.setValue(value)
    Player.get_instance().volume = value
    if value == 0:
        ui.mute.setIcon(QIcon("Grafiki/Mute-mowp.png"))
    else:
        ui.mute.setIcon(QIcon("Grafiki/Speaker-mowp.png"))


def value_changed(value):
    if value == 99:
        set_volume(100)
    else:
        set_volume(value)

playlist = Playlist([])
def wczytaj_onclick():
    from PyQt5.QtWidgets import QWidget
    import os
    global ui, playlist

    class Widget(QWidget):
        def __init__(self):
            super().__init__()

        def showDialog(self):
            fileName, _ = QFileDialog.getOpenFileName(self, 'Wczytaj playlistę', '/home',
                                                      filter="Mowp file (*.mowp.xml)")
            playlist = PlaylistFile.open(str(fileName))
            model = QStringListModel()
            supp = model.supportedDragActions()
            #model.fl

            playlist2 = []
            for track in playlist:
                playlist2.append(str(track))
            model.setStringList(playlist2)
            ui.playlista.setModel(model)

    widget = Widget()
    widget.showDialog()


def mute_clicked():
    global ui, old_volume
    if Player.get_instance().volume == 0:
        set_volume(old_volume)
        ui.mute.setIcon(QIcon('Grafiki/Speaker-mowp.png'))

    else:
        old_volume = Player.get_instance().volume
        set_volume(0)

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


class Signal(QObject):
    signal = pyqtSignal()

    def connect(self,func):
        self.signal.connect(func)

    def emit(self):
        self.signal.emit()


def format(czas):
    if czas < 10:
        return "0{}".format(czas)
    return czas

def ustaw_czas_calkowity(args):
    args["user"]["czasCalkowity"].setText("/{}:{}".format(format(int(args["length"] / 60)), format(int(args["length"] % 60))))

czas_qtimer = QTimer()

def trackUp_clicked():
    global ui
    items = ui.playlista.selectionModel().selectedIndexes()
    if len(items) > 0:
        list = ui.playlista.model().stringList()
        if items[0].row() == 0:
            return
        object = list[items[0].row()-1]
        list[items[0].row()-1] = list[items[0].row()]
        list[items[0].row()] = object

        ui.playlista.model().setStringList(list)
        playlist.track_change_place(track=items[0].row(), number=items[0].row()-1)

def trackDown_clicked():
    global ui
    items = ui.playlista.selectionModel().selectedIndexes()
    if len(items) > 0:
        list = ui.playlista.model().stringList()
        if items[0].row() == len(list)-1:
            return
        object = list[items[0].row()]
        list[items[0].row()] = list[items[0].row()+1]
        list[items[0].row()+1] = object

        ui.playlista.model().setStringList(list)
        playlist.track_change_place(track=items[0].row(), number=items[0].row()+1)


def timer_start():
    global  czas_qtimer
    czas_qtimer.start(1000)


czas = 0
def co_sekunde_ustaw_czas(event=None):
    global ui
    czas = Player.get_instance().time
    ui.label.setText("{}:{}".format(format(int(czas/60)), format(int(czas%60))))


def ustaw_czas(args):
    global czas_qtimer
    ui.label.setText("00:00")
    czas_qtimer.timeout.connect(co_sekunde_ustaw_czas)
    signal = Signal()
    signal.emit()

playlist = Playlist([])

def dodaj_clicked():
    global ui, playlist
    list = ui.treeView.selectionModel().selectedIndexes()
    model = ui.treeView.model()
    row = -1
    for index in list:
        if index.row() != row and index.column() == 0:
            fileInfo = model.fileInfo(index)
            playlist.add_track(Track(str(fileInfo.filePath())))
            list = ui.playlista.model().stringList()
            list.append(str(fileInfo.filePath()))
            ui.playlista.model().setStringList(list)
            row = index.row()

def remove_clicked():
    global ui
    items = ui.playlista.selectionModel().selectedIndexes()
    if len(items) > 0:
        list = ui.playlista.model().stringList()
        del list[items[0].row()]
        ui.playlista.model().setStringList(list)
        playlist.remove_track(number=items[0].row())

def zapisz_clicked():

        from PyQt5.QtWidgets import QWidget
        import os
        global ui, playlist

        class Widget(QWidget):
            def __init__(self):
                super().__init__()

            def showDialog(self):
                if len(playlist) == 0:
                    msgBox = QMessageBox()
                    msgBox.setText("Pusta playlista!")
                    msgBox.exec()
                    return
                fileName, _ = QFileDialog.getSaveFileName(self, 'Wczytaj playlistę', '/home',
                                                          filter="Mowp file (*.mowp.xml)")
                PlaylistFile.write(fileName, playlist)


        widget = Widget()
        widget.showDialog()

def MyEvent(QEvent):
    pass

if __name__ == "__main__":
    import sys
    global app
    app = QtWidgets.QApplication(sys.argv)
    global MainWindow
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
    ui.ciemny.clicked.connect(ciemny_click)
    ui.jasny.clicked.connect(jasny_click)
    EventManager.get_instance().add_event(Event.MediaPaused, ustaw_play, {"playPause": ui.playPause})
    EventManager.get_instance().add_event(Event.MediaPlay, ustaw_pauza, {"playPause": ui.playPause})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_play, {"playPause": ui.playPause})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_tytul, {"tytul": ui.label_3})
    EventManager.get_instance().add_event(Event.MediaPlay, ustaw_czas_calkowity, {"czasCalkowity": ui.czasCalkowity})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_czas_calkowity, {"czasCalkowity": ui.czasCalkowity})
    EventManager.get_instance().add_event(Event.MediaStarted, ustaw_czas)
    signal = Signal()
    signal.connect(timer_start)
    ui.next.clicked.connect(next_clicked)
    ui.previous.clicked.connect(previous_clicked)
    ui.listaRadio.clicked.connect(lista_clicked)
    ui.stop.clicked.connect(stop_clicked)
    ui.dodaj.clicked.connect(dodaj_clicked)
    model.setRootPath(QDir.homePath())
    model.sort(0)
    model.setNameFilters(["*.mp3", ".ogg"])
    model.setNameFilterDisables(False)
    ui.playlista.setDragEnabled(True)
    ui.playlista.viewport().setAcceptDrops(True)
    ui.treeView.setModel(model)
    ui.treeView.setRootIndex(model.setRootPath(QDir.homePath()))
    ui.treeView.hideColumn(1)
    ui.treeView.hideColumn(2)
    ui.treeView.hideColumn(3)
    ui.treeView.hideColumn(4)
    ui.playlista.setModel(QStringListModel())
    ui.playlista.setEditTriggers(QAbstractItemView.NoEditTriggers)
    ui.remove.clicked.connect(remove_clicked)
    ui.trackUp.clicked.connect(trackUp_clicked)
    ui.trackDown.clicked.connect(trackDown_clicked)
    ui.zapisz.clicked.connect(zapisz_clicked)
    MainWindow.show()
    global playlist
    playlist = Playlist(["/home/mat-bi/tb.mp3"])
    player.current_playlist = playlist
    player.play_track()
    global czas_qtimer
    ui.label.setText("00:00")
    czas_qtimer.timeout.connect(co_sekunde_ustaw_czas)
    czas_qtimer.start()
    sys.exit(app.exec_())


