import threading
from Track import Track
from sys import stderr
import Player
import random
import time


class Playlist():
    def __init__(self, lista):
        list = []
        for i in lista:
            if isinstance(i, Track):
                list.append(i)
            else:
                list.append(Track(i))
        self._list = list
        # stderr.write(str(list))
        # stderr.flush()
        self._current = None
        self._index = 0
        '''if len(lista) > 0:
            self._current = self._list[0]
        else:
            self._current = None'''
        # stderr.write("{}\n".format(str(lista)))
        stderr.flush()
        self.rlock = threading.RLock()

    def add_track(self, track):
        with self.rlock:
            if not isinstance(track, Track):
                track = Track(track)
            self._list.append(track)
            if len(self._list) == 1:
                self._current = self._list[0]

    def remove_track(self, track=None, number=None):
        with self.rlock:
            if isinstance(track, Track):
                ind = self._list.index(track)
                if ind < self._index:
                    self._index -= 1
                self._list.remove(track)
            elif isinstance(number, int):
                if number < self._index:
                    self._index -= 1
                del self._list[number]

    def current(self):
        with self.rlock:
            if self._current is None and len(self._list) > 0:
                self._current = self._list[0]
                self._index = 0
            return self._current

    def next(self, opt):
        with self.rlock:
            if opt == Player.Player_Ops.RepeatTrack:
                pass
            elif opt == Player.Player_Ops.RepeatPlaylist and self._index == len(self._list) - 1:
                self._index = 0
                self._current = self._list[0]
            elif opt == Player.Player_Ops.Normal and self._index == len(self._list) - 1:
                self._current = None
                return self._current
            elif opt == Player.Player_Ops.RandomTrack:
                self._index = random.randint(0, len(self._list) - 1)
                self._current = self._list[self._index]
            else:
                self._index += 1
                self._current = self._list[self._index]
            return self.current()

    def previous(self):
        with self.rlock:
            if self._index > 0:
                self._index -= 1
                self._current = self._list[self._index]
            else:
                self._index = 0
                self._current = self._list[0]
            return self.current()

    def selected(self, number):
        with self.rlock:
            self._current = self._list[number]
            return self.current()

    def __len__(self):
        with self.rlock:
            return len(self._list)

    def __iter__(self):
        with self.rlock:
            return iter(self._list)

    def track_change_place(self, track, number):
        with self.rlock:
            t = self._list[track]
            self._list[track] = None
            self._list.insert(number, t)
            self._list.remove(None)

    '''def __getitem__(self, item):
        with self.rlock:
            return self._list[item]

    def __setitem__(self, key, value):
        with self.rlock:
            self._list[key] = value'''
