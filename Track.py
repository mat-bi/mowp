from mutagen.easyid3 import EasyID3
from mutagen import File
import os


class Track:
    def __init__(self, path):
        self._path = path
        try:
            self.info = EasyID3(path)
        except:
            title = []
            title.append(os.path.basename(path))

            self.info = {"artist": ["Nieznany wykonawca"], "title": title}
        try:
            self.length = File(path).info.length
        except:
            self.length = 0

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __getitem__(self, item):
        if self.info is None:
            return None
        if item == "artist":
            if isinstance(self.info, EasyID3):
                if self.info.get("artist") is None:
                    return ["Nieznany wykonawca"]
                else:
                    return self.info.get("artist")
            else:
                return [self.info["artist"]]
        elif item == "length":
            if self.length is None:
                return 0
            else:
                return self.length
        elif item == "title":
            if isinstance(self.info, EasyID3):
                if self.info.get("title") is None:
                    return str(os.path.basename(self._path))
                else:
                    return self.info.get("title")
            else:
                return list(self.info["title"])
        else:
            return None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.path == self.path
        return False

    def __str__(self):
        return self._path
