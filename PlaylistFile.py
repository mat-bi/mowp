import xml.etree.cElementTree as ET
from Playlist import Playlist
import os


class PlaylistFile:
    @staticmethod
    def open(path):
        tree = ET.parse(path)
        root = tree.getroot()
        playlist = Playlist([])
        for child in root:
            if os.path.exists(child.text):
                playlist.add_track(child.text)
        return playlist

    @staticmethod
    def write(path, playlist):
        element = ET.Element("tracks")
        tree = ET.ElementTree(element=element)
        for track in playlist:
            sub = ET.SubElement(element, "track")
            sub.text = str(track)
        tree.write(path)
