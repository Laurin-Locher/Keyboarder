import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from src.widgets.slider import Slider


class Drums(ctk.CTkFrame):
    def __init__(self, master, bg, synth, bpm):
        self.background = bg
        self.bpm = bpm
        self.synth = synth

        super().__init__(master, fg_color=bg)
        self.beat = 16
        self.current_beat_index = 0
        self.base_beat = self.beat * [False]
        self.hi_hat_beat = self.beat * [False]
        self.snare_beat = self.beat * [False]

        self.base_soundfile = 'resource/Drums/BlueRidge/Base_drum.wav'
        self.snare_soundfile = 'resource/Drums/BlueRidge/Snare.wav'
        self.hi_hat_soundfile = 'resource/Drums/BlueRidge/Hi-Hat.wav'

        self.update_elements = []
        self.create_gui()

    def to_dict(self):
        return {
            'base_beat': self.base_beat,
            'hi_hat_beat': self.hi_hat_beat,
            'snare_beat': self.snare_beat
        }

    def from_dict(self, dict_):
        try:
            self.base_beat.clear()
            self.base_beat.extend(dict_['base_beat'])
            self.hi_hat_beat.clear()
            self.hi_hat_beat.extend(dict_['hi_hat_beat'])
            self.snare_beat.clear()
            self.snare_beat.extend(dict_['snare_beat'])

        except KeyError:
            messagebox.showerror(title='File Error', message="File is invalid")

        for update in self.update_elements:
            update()

    def tick(self):
        if self.base_beat[self.current_beat_index]:
            self.synth.start_sound_file(self.base_soundfile, self.volume.get())

        if self.snare_beat[self.current_beat_index]:
            self.synth.start_sound_file(self.snare_soundfile, self.volume.get())

        if self.hi_hat_beat[self.current_beat_index]:
            self.synth.start_sound_file(self.hi_hat_soundfile, self.volume.get())

        self.current_beat_index = (self.current_beat_index + 1) % self.beat

    def create_gui(self):
        self.columnconfigure(0, weight=12)
        self.columnconfigure(1, weight=1)

        self.rowconfigure((0, 1, 2), weight=1, uniform='a')

        self.base_drum_frame = ctk.CTkFrame(self, border_width=1, fg_color=self.background)
        self.hi_hat_frame = ctk.CTkFrame(self, border_width=1, fg_color=self.background)
        self.snare_frame = ctk.CTkFrame(self, border_width=1, fg_color=self.background)

        self.volume = ctk.DoubleVar(value=3)

        from src.app import ACCENT_COLOR, DISABLED_COLOR, DARK_COLOR
        self.volume_slider = Slider(self, orientation='vertical', from_=0, to=5, variable=self.volume, fg_color=DARK_COLOR, bg_color=DISABLED_COLOR, has_handle=True, handle_color=ACCENT_COLOR, slider_width=4, handle_width=15, handle_height=5)
        self.volume_slider.grid(row=0, column=1, rowspan=3, sticky='nswe')

        self.base_drum_frame.grid(row=0, column=0, sticky='nswe')
        self.hi_hat_frame.grid(row=1, column=0, sticky='nswe')
        self.snare_frame.grid(row=2, column=0, sticky='nswe')

        self.icons_path = 'resource/symbols/Drum_icons'

        base_drum_icon = self.load_icon('Base_drum.png')
        snare_icon = self.load_icon('Snare.png')
        hi_hat_icon = self.load_icon('Hi-Hat.png')

        base_drum_pattern = self.create_pattern(self.base_drum_frame, base_drum_icon, self.base_beat)
        base_drum_pattern.pack(expand=True, fill='both', padx=5, pady=5)

        hi_hat_pattern = self.create_pattern(self.hi_hat_frame, hi_hat_icon, self.hi_hat_beat)
        hi_hat_pattern.pack(expand=True, fill='both', padx=5, pady=5)

        snare_pattern = self.create_pattern(self.snare_frame, snare_icon, self.snare_beat)
        snare_pattern.pack(expand=True, fill='both', padx=5, pady=5)

    def load_icon(self, icon: str):
        return ctk.CTkImage(light_image=Image.open(f'{self.icons_path}/black/{icon}'),
                            dark_image=Image.open(f'{self.icons_path}/white/{icon}')
                            )

    def create_pattern(self, master, image, beat_array):
        frame = ctk.CTkFrame(master, fg_color=self.background)
        title = ctk.CTkLabel(frame, text='', image=image)
        title.pack(side='left', fill='y', padx=10)

        pattern = ctk.CTkFrame(frame, fg_color=self.background)

        beats = tuple(range(self.beat))

        pattern.columnconfigure(beats, weight=1, uniform='a')
        pattern.rowconfigure(0, weight=1, uniform='a')

        from src.app import ACCENT_COLOR, DISABLED_COLOR
        enabled_color = ACCENT_COLOR
        disabled_color = DISABLED_COLOR

        for beat_index in beats:
            beat = beat_array[beat_index]
            if beat:
                current_color = enabled_color

            else:
                current_color = disabled_color

            beat_button = ctk.CTkFrame(pattern, fg_color=current_color, corner_radius=5, border_width=5,
                                       border_color=self.background)
            beat_button.grid(row=0, column=beat_index, sticky='nswe')

            beat_button.bind('<Button>',
                             lambda _, b=beat_button, i=beat_index, ba=beat_array:
                             self.toggle_beat(b, i, ba, enabled=enabled_color, disabled=disabled_color))

            if beat_array is self.base_beat:
                self.update_elements.append(lambda b=beat_button, i=beat_index:
                                            self.update_beat(b, i, self.base_beat,
                                                             enabled=enabled_color,
                                                             disabled=disabled_color))

            elif beat_array is self.hi_hat_beat:
                self.update_elements.append(lambda b=beat_button, i=beat_index:
                                            self.update_beat(b, i, self.hi_hat_beat,
                                                             enabled=enabled_color,
                                                             disabled=disabled_color))

            elif beat_array is self.snare_beat:
                self.update_elements.append(lambda b=beat_button, i=beat_index:
                                            self.update_beat(b, i, self.snare_beat,
                                                             enabled=enabled_color,
                                                             disabled=disabled_color))

        pattern.pack(expand=True, fill='both')

        return frame

    @staticmethod
    def toggle_beat(element, index, beat, enabled, disabled):

        beat[index] = not beat[index]

        if beat[index]:
            element.configure(fg_color=enabled)

        else:
            element.configure(fg_color=disabled)

    @staticmethod
    def update_beat(element, index, beat_array, enabled, disabled):
        if beat_array[index]:
            element.configure(fg_color=enabled)

        else:
            element.configure(fg_color=disabled)
