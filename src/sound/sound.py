import numpy as np
import numba


NOTES = {
    'A': 27.500,
    'A#': 29.135,
    'B': 30.868,
    'C': 32.703,
    'C#': 34.648,
    'D': 36.708,
    'D#': 38.891,
    'E': 41.203,
    'F': 43.654,
    'F#': 46.249,
    'G': 48.999,
    'G#': 51.913,
}


def transpose(note, octave, delta) -> tuple[str, int]:
    names = list(NOTES.keys())
    note_index = names.index(note) + delta
    while note_index < 0:
        note_index += len(names)
        octave -= 1

    while note_index >= len(names):
        note_index -= len(names)
        octave += 1

    return names[note_index], octave

@numba.njit
def adsr(volume_buf, t, sample_rate, length, volume, attack, decay, t_release, sustain, release):
    for i in range(length):
        if t < attack:
            volume_buf[i] = t / attack * volume
        elif t < attack + decay:
            x = (t - attack) / decay
            volume_buf[i] = (1 - x) * volume + x * release * volume
        elif t < t_release:
            volume_buf[i] = release * volume
        elif sustain > 0:
            x = (t - t_release) / sustain
            volume_buf[i] = max(0, (1 - x) * release * volume)
        else:
            volume_buf[i] = 0
        t = t + 1 / sample_rate


@numba.njit
def smoothclip(buf):
    for i in range(len(buf)):
        if buf[i] < -1.5:
            buf[i] = -1
        elif buf[i] > 1.5:
            buf[i] = 1
        else:
            x = buf[i]
            buf[i] = x * (27 - 4 * x * x) / 27


class Sound:
    def __init__(self, note: str, octave: int, parameters):

        self.parameters = parameters

        self._t = .0
        self._note_octave = (note, octave)
        self._freq = NOTES[note] * 2 ** octave
        self._t_release = float('inf')
        self._volume_buf = None
        self._sum_buf = None

        if not self.parameters.hold:
            self.release()

    def get_note_octave(self):
        return self._note_octave

    def generate(self, buf, sample_rate: int, length: int):
        if self._volume_buf is None or len(self._volume_buf) != length:
            self._volume_buf = np.empty((length,), dtype=np.float32)
            self._sum_buf = np.empty((length,), dtype=np.float32)
        adsr(
            self._volume_buf, self._t, sample_rate, length,
            self.parameters.volume, self.parameters.attack, self.parameters.decay, self._t_release, self.parameters.sustain, self.parameters.release)
        t_buf = np.arange(length) / sample_rate + self._t
        self._t += length / sample_rate

        self._sum_buf[:] = 0
        for i, weight in enumerate(self.parameters.overtones):
            self._sum_buf[:] += weight * np.sin(t_buf * 2 * (i + 1) * np.pi * self._freq).astype(np.float32)
        buf[:] += self._volume_buf * self._sum_buf

        return self._t < self._t_release + self.parameters.sustain

    def release(self):
        if np.isinf(self._t_release):
            self._t_release = max(self.parameters.attack + self.parameters.decay, self._t)


# precompile numba functions
adsr(np.empty((8,), dtype=np.float32), .0, 8, 8, .0, .0, .0, .0, .0, .0)
smoothclip(np.ones((8,), dtype=np.float32))
