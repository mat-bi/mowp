from Ops import *
import vlc
import time
from EventManager import *
from Event import *
from Player import *
from sys import stderr

class VlcThread(threading.Thread):
    def __init__(self, player):
        threading.Thread.__init__(self)
        self.player = player

    def run(self):
        z = False
        instance = vlc.Instance()
        p = vlc.MediaPlayer(str(self.player.current_playlist.current()))
        track = self.player.current_playlist.current()
        while True:
            with self.player.rlock:
                try:
                    p.audio_set_volume(self.player.volume)
                except:
                    pass
                try:
                    self.player._time = int(p.get_position() * track["length"])
                except:
                    pass
                a = p.get_media().get_state()
                if self.player._op == Ops.ChangeTrack:
                    self.player._op = Ops.Done
                    p.stop()
                    track = self.player.current_playlist.current()
                    p = vlc.MediaPlayer(str(track))
                elif a == 6:
                    self.player._time = 0
                    track = self.player.current_playlist.next(self.player.playlist_opt)
                    p = vlc.MediaPlayer(str(track))
                    if track is None:
                        EventManager.get_instance().trigger_event(Event.PlaylistEnded)
                    else:
                        p.play()
                        EventManager.get_instance().trigger_event(Event.MediaStarted,
                                                                  {"title": track["title"], "length": track["length"]})
                elif a == 0 and self.player._op == Ops.Play:
                    self.player._op = Ops.Done
                    p.play()
                    EventManager.get_instance().trigger_event(Event.MediaStarted,
                                                              {"title": track["title"], "length": track["length"]})
                elif self.player._op == Ops.NoOp or self.player._op == Ops.Done:
                    pass
                else:
                    op = self.player._op
                    self.player._op = Ops.Done
                    if op == Ops.Play and track != self.player.current_playlist.current():
                        track = self.player.current_playlist.current()
                        p = vlc.MediaPlayer(str(track))
                        p.play()
                        EventManager.get_instance().trigger_event(Event.MediaStarted, {"title": track["title"],
                                                                                       "length": track["length"]})
                    elif op == Ops.Play and a != 3:
                        if a != 4:
                            track = self.player.current_playlist.current()
                            p = vlc.MediaPlayer(str(track))
                        p.play()
                        if a == 4:
                            EventManager.get_instance().trigger_event(Event.MediaStarted, {"title": track["title"],
                                                                                           "length": track["length"]})
                        else:
                            EventManager.get_instance().trigger_event(Event.MediaPlay, {"title": track["title"],
                                                                                        "length": track["length"]})
                    elif op == Ops.Pause and a != 4:
                        p.pause()
                        EventManager.get_instance().trigger_event(Event.MediaPaused)
                    elif op == Ops.Pause:
                        p.play()
                        EventManager.get_instance().trigger_event(Event.MediaPlay,
                                                                  {"title": track["title"], "length": track["length"]})
                    elif op == Ops.ChangePlaylist:
                        p.stop()
                        track = self.player.current_playlist.current()
                        p = vlc.MediaPlayer(str(track))
                        # EventManager.get_instance().trigger_event(Event.MediaStopped)
                    elif op == Ops.ChangeVolume:
                        p.audio_set_volume(self.player.volume)
                        EventManager.get_instance().trigger_event(Event.VolumeChanged)
                        # elif
                    elif op == Ops.Stop:
                        p.stop()
                        EventManager.get_instance().trigger_event(Event.MediaStopped)
                    elif op == Ops.TimeChanged:
                        self.player._time = self.player._changed_time
                        if track is None:
                            pass
                        elif (self.player._changed_time >= track["length"]):
                            p.set_position(1.0)
                            z = True
                        else:
                            p.set_position(self.player._changed_time / track["length"])
                            EventManager.get_instance().trigger_event(Event.TimeChanged,
                                                                      {"time": self.player._changed_time,
                                                                       "length": track["length"]})
                        # EventManager.get_instance().trigger_event(Event.Event.MediaEnded)
            try:
                self.player.lock.release()
                self.player.lock.release()
            except RuntimeError:
                pass
            time.sleep(0.001)
