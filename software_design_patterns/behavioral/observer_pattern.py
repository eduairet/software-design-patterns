import time

END_OF_QUEUE_LOG = "No more songs in the queue."
NOW_PLAYING_LOG = lambda song: (
    f"Now playing: {song.title} by {song.artist} | Time: {song.current_time}/{song.time}"
)
NEXT_SONG_LOG = lambda song: (
    f"Next song: {song.title} by {song.artist}" if song else END_OF_QUEUE_LOG
)


class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


class PropertyObservable:
    def __init__(self):
        self.property_changed = Event()
        return self


class Song:
    def __init__(self, title: str, artist: str, time: int):
        self.title = title
        self.artist = artist
        self.time = time
        self.current_time = 0


class Radio(PropertyObservable):
    def __init__(self):
        super().__init__()
        self.queue = []
        self._now_playing = None
        self.log = []

    def now_playing_msg(self):
        self.property_changed("now_playing", self._now_playing)
        self.log.append(NOW_PLAYING_LOG(self._now_playing))

    def next_song_msg(self):
        self.property_changed("next_song", self._now_playing)
        self.log.append(NEXT_SONG_LOG(self._now_playing))

    def end_of_queue_msg(self):
        self.property_changed("end_of_queue")
        self.log.append(END_OF_QUEUE_LOG)

    def add_song(self, song: Song):
        self.queue.append(song)
        return self

    def play(self):
        if not self.queue:
            self.end_of_queue_msg()
            return

        while self.queue:
            self._now_playing = self.queue[0]

            while not self.next_song:
                time.sleep(1)
                self._now_playing.current_time += 1
                self.now_playing_msg()

            self.queue.pop(0)
            if self.queue:
                self._now_playing = self.queue[0]
                self.next_song_msg()
            else:
                self.end_of_queue_msg()

    @property
    def next_song(self):
        return self._now_playing.current_time >= self._now_playing.time


def song_changed(event: str, song: Song = None):
    if event == "next_song":
        print(NEXT_SONG_LOG(song))
    elif event == "now_playing":
        print(NOW_PLAYING_LOG(song))
    elif event == "end_of_queue":
        print(END_OF_QUEUE_LOG)
