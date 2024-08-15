import customtkinter as ctk
from src.widgets.key import Key


class Keyboard(ctk.CTkFrame):
    def __init__(self, master, synth, keyboardVisualizer):
        super().__init__(master)

        self.synth = synth

        notes = []
        for binding in self.synth.KEY_BINDING:
            notes.append(self.synth.KEY_BINDING[binding])
        number_of_white_keys = 0

        for note, _ in notes:
            if len(note) == 1:
                number_of_white_keys += 1

        rel_key_width = 1 / number_of_white_keys
        key_pos = 0
        self.keys = {}
        black_keys = []

        for note in notes:
            if len(note[0]) == 1:
                key = Key(self, 'white', note, keyboardVisualizer)
                key.place(relx=key_pos, rely=0, relheight=1, relwidth=rel_key_width)

                key_pos += rel_key_width

                self.keys[note] = key

            else:
                key = Key(self, 'black', note, keyboardVisualizer)
                width = rel_key_width * 0.5
                x = key_pos - rel_key_width / 4
                key.place(relx=x, rely=0, relheight=0.65, relwidth=width)
                black_keys.append(key)

                self.keys[note] = key

            for key in black_keys:
                key.lift()
