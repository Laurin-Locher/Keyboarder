import pyaudio
import numpy as np
from threading import Lock
from src.sound.sound import Sound, smoothclip
from src.KeyboardVisualizer import KeyboardVisualizer
from src.sound.SoundFile import SoundFile
from src.sound.arpeggio import Arpeggio

SAMPLE_RATE = 44100


class Synth:
    KEY_BINDING = {
        'a': ('B', 0),
        's': ('C', 0),
        'e': ('C#', 0),
        'd': ('D', 0),
        'r': ('D#', 0),
        'f': ('E', 0),
        'g': ('F', 0),
        'z': ('F#', 0),
        'h': ('G', 0),
        'u': ('G#', 0),
        'j': ('A', 1),
        'i': ('A#', 1),
        'k': ('B', 1),
        'l': ('C', 1),
        'p': ('C#', 1),
        'ö': ('D', 1),
        'ü': ('D#', 1),
        'ä': ('E', 1),
        '$': ('F', 1)
    }

    def __init__(self, octave, window, keyboardVisualizer: KeyboardVisualizer, update_octave):
        self._pa = pyaudio.PyAudio()
        self._stream = None
        self._call_tick_every = 0
        self._callback_count = 0
        self._tick_subscribers = set()
        self.set_bpm(120)
        self._octave = octave
        self._sounds = set()
        self._arpeggios = set()
        self._lock = Lock()
        self._pressed_keys = set()
        self._keyboardVisualizer = keyboardVisualizer
        self._update_octave = update_octave

        self.window = window

    def _start_stream(self, samples_per_callback):
        self._stream = self._pa.open(
            rate=SAMPLE_RATE, channels=1, format=pyaudio.paFloat32, output=True,
            stream_callback=self._stream_callback, frames_per_buffer=samples_per_callback)
        self._buffer = np.zeros((samples_per_callback,), dtype=np.float32)
        self._stream.start_stream()

    def add_tick_subscriber(self, subscriber):
        self._tick_subscribers.add(subscriber)

    def remove_tick_subscriber(self, subscriber):
        self._tick_subscribers.remove(subscriber)

    def set_bpm(self, bpm):
        samples_per_callback = 60 * SAMPLE_RATE // bpm // 4
        self._call_tick_every = 1
        self._callback_count = 0
        while samples_per_callback > 2048:
            samples_per_callback //= 2
            self._call_tick_every *= 2
        if self._stream is not None:
            self._stream.close()
        self._start_stream(samples_per_callback)

    def change_octave(self, amount: int):
        self._octave += amount
        self._update_octave(self._octave)

    def set_octave(self, amount: int):
        self._octave = amount
        self._update_octave(self._octave)

    def stop_all(self):
        with self._lock:
            for sound in self._sounds:
                sound.release()

        for arpeggio in self._arpeggios:
            arpeggio.release()

    def get_buffer(self):
        with self._lock:
            return self._buffer.copy()

    def _notify_tick_subscribers(self):
        for subscriber in self._tick_subscribers:
            subscriber.tick()
        for arpeggio in self._arpeggios:
            arpeggio.tick()

    def _stream_callback(self, in_data, frame_count, time_info, status):
        if self._callback_count == 0:
            self._notify_tick_subscribers()
        self._callback_count = (self._callback_count + 1) % self._call_tick_every
        with self._lock:
            self._buffer[:] = 0
            sounds_to_remove = set()
            for sound in self._sounds:
                if not sound.generate(self._buffer, SAMPLE_RATE, frame_count):
                    sounds_to_remove.add(sound)
            for sound in sounds_to_remove:
                self._sounds.remove(sound)
            smoothclip(self._buffer)
        return self._buffer, pyaudio.paContinue

    def _key_down(self, event):
        if event.char in self._pressed_keys:
            return
        self._pressed_keys.add(event.char)

        try:
            note = self.KEY_BINDING[event.char.lower()]
            self._keyboardVisualizer.key_down(note)
        except KeyError:
            pass

    def start_sound(self, note, octave_increment, parameters, sound_list=None, offset_octave=True):
        if sound_list:
            self._arpeggios.add(Arpeggio(note, octave_increment, parameters, sound_list, self, offset_octave))
        else:
            with self._lock:
                if offset_octave:
                    octave = self._octave + octave_increment
                else:
                    octave = octave_increment

                sound = Sound(note, octave, parameters)
                self._sounds.add(sound)
                return sound

    def start_sound_file(self, filename, volume):
        with self._lock:
            self._sounds.add(SoundFile(filename, volume))

    def _key_up(self, event):
        try:
            self._pressed_keys.remove(event.char)
            note = self.KEY_BINDING[event.char.lower()]
            self._keyboardVisualizer.key_up(note)
        except KeyError:
            pass

    def stop_sound(self, note, octave_increment, offset_octave=True):
        if offset_octave:
            octave = self._octave + octave_increment
        else:
            octave = octave_increment

        for sound in self._sounds:
            if sound.get_note_octave() == (note, octave):
                sound.release()

        arpeggios_to_remove = []
        for arpeggio in self._arpeggios:
            if arpeggio.get_note_octave() == (note, octave_increment):
                arpeggio.release()
                arpeggios_to_remove.append(arpeggio)
        for arpeggio in arpeggios_to_remove:
            self._arpeggios.remove(arpeggio)

    def run(self):
        self.window.bind('<KeyPress>', self._key_down)
        self.window.bind('<KeyRelease>', self._key_up)
