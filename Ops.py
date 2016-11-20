from enum import Enum


class Ops(Enum):
    NoOp = -1
    Done = 0
    ChangeVolume = 1
    ChangePlaylist = 2
    Play = 3
    Pause = 4
    Stop = 5
    ChangeTrack = 6
    TimeChanged = 7
