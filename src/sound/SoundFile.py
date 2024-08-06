import wave
import numpy as np


class SoundFile:

    def __init__(self, filename, volume):
        self._volume = volume
        self._wave_file = wave.open(filename, 'rb')

    def generate(self, buf, sample_rate: int, length: int):
        assert (self._wave_file.getframerate() == sample_rate)
        data = np.frombuffer(self._wave_file.readframes(length), dtype=np.int16)
        data = data[::self._wave_file.getnchannels()]
        buf[:len(data)] += data.astype(np.float32) / 32768 * self._volume
        return len(data) == length

    @staticmethod
    def get_note_octave():
        return None
