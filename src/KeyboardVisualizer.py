
class KeyboardVisualizer:

    def key_down(self, note: (str, int), is_midi_input: bool):
        raise NotImplemented

    def key_up(self, note: (str, int)):
        raise NotImplemented
