import wave
import numpy as np


class SoundFile:
    CACHE = {}

    def __init__(self, filename, volume):
        self._volume = volume

        if filename not in self.CACHE:
            from src.sound.synth import SAMPLE_RATE
            wf = wave.open(filename, mode='rb')
            print(f'loading {filename}')
            assert wf.getframerate() == SAMPLE_RATE
            data = wf.readframes(wf.getnframes())
            data = np.frombuffer(data, dtype=np.int16)
            data = data[::wf.getnchannels()]
            data = data.astype(np.float32) / 32768
            self.CACHE[filename] = data
        self._data = self.CACHE[filename]
        self._pos = 0

    def generate(self, buf, sample_rate: int, length: int):
        if self._volume == 0:
            return False

        remaining = min(length, len(self._data) - self._pos)
        buf[:remaining] += self._data[self._pos: self._pos + remaining] * self._volume
        self._pos += remaining
        return remaining == length

    @staticmethod
    def get_note_octave():
        return None
