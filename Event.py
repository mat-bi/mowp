from enum import Enum


class Event(Enum):
    MediaEnded = 0
    MediaPlay = 1
    MediaPaused = 2
    MediaStopped = 3
    MediaStarted = 4
    PlaylistEnded = 5
    PlaylistPlay = 6
    VolumeChanged = 7
    TimeChanged = 8
