from src.sound.sound import transpose


class Arpeggio:
    def __init__(self, note: str, octave: int, parameters, sound_list, synth, offset_octave):
        self.note = note
        self.octave = octave
        self.offset_octave: bool = offset_octave
        self.parameters = parameters
        self.sound_list = sound_list
        self.synth = synth
        self.last_sound = None

        self.play_pos = 0

    def release(self):
        if self.last_sound:
            self.last_sound.release()

    def tick(self):
        delta = self.sound_list[self.play_pos]

        if delta is not None:
            if self.last_sound:
                self.last_sound.release()

            note, octave = transpose(self.note, self.octave, delta)

            self.last_sound = self.synth.start_sound(note, octave, self.parameters, offset_octave=self.offset_octave)

        self.play_pos = (self.play_pos + 1) % len(self.sound_list)

    def get_note_octave(self):
        return self.note, self.octave
