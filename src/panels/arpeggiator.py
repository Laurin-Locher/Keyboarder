import customtkinter as ctk
from src.widgets.slider import Slider


class Arpeggiator(ctk.CTkFrame):
    def __init__(self, master, bg):
        self.background = bg
        super().__init__(master, fg_color=self.background)

        self.total_number_of_tones = 16
        self.number_of_tones = ctk.IntVar(value=0)
        self.tones = []
        self.tone_sliders = []

        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=4, uniform='a')
        self.rowconfigure(2, weight=2, uniform='a')
        self.rowconfigure(3, weight=1, uniform='a')
        # self.test_slider = ctk.CTkSlider(self)

        title = ctk.CTkLabel(self, text='Arpeggiator')
        title.grid(row=0, column=0, sticky='nswe')

        self.columnconfigure(list(range(self.total_number_of_tones)), weight=1, uniform='a')

        for index in range(self.total_number_of_tones):
            tone = ctk.IntVar()
            duration = ctk.IntVar()
            self.tones.append((tone, duration))

            self.slider(tone, duration, index, 1)

        number_of_tones_slider = ctk.CTkSlider(self, orientation='horizontal', variable=self.number_of_tones, from_=0,
                                               to=self.total_number_of_tones,
                                               number_of_steps=self.total_number_of_tones + 1)
        number_of_tones_slider.grid(row=4, column=0, sticky='nwe', columnspan=self.total_number_of_tones)

        self.number_of_tones.trace_add('write', self.update_sliders)
        self.update_sliders()

    def to_dict(self):
        notes = []
        durations = []
        for note, duration in self.tones:
            notes.append(note.get())
            durations.append(duration.get())

        return {
            'notes': notes,
            'durations': durations,
            'number_of_tones': self.number_of_tones.get()
        }

    def from_dict(self, dict_):
        for index, (note, duration) in enumerate(zip(dict_['notes'], dict_['durations'])):
            self.tones[index][0].set(note)
            self.tones[index][1].set(duration)

        self.number_of_tones.set(dict_['number_of_tones'])

    def update_sliders(self, *args):
        for index, sliders in enumerate(self.tone_sliders):
            for slider in sliders:
                if index >= self.number_of_tones.get():
                    slider.disable()

                else:
                    slider.enable()

    def slider(self, tone, duration, column, row):

        from src.app import ACCENT_COLOR, DISABLED_COLOR, DARK_COLOR
        tone_slider = Slider(self, orientation='vertical', variable=tone, from_=-12, to=12, number_of_steps=24,
                             has_handle=True, slider_width=4, handle_width=15, handle_height=5, fg_color=DARK_COLOR,
                             handle_color=ACCENT_COLOR, bg_color=DISABLED_COLOR, start_in_middle=True)

        duration_slider = Slider(self, orientation='vertical', variable=duration, from_=1, to=4,
                                 number_of_steps=3, has_handle=True, slider_width=4, handle_width=15, handle_height=5,
                                 fg_color=DARK_COLOR, handle_color=ACCENT_COLOR, bg_color=DISABLED_COLOR)
        title_label = ctk.CTkLabel(self, text='title')

        tone_slider.grid(row=row, column=column, sticky='nsw', pady=10)
        duration_slider.grid(row=row + 1, column=column, sticky='nsw', pady=10)

        self.tone_sliders.append((tone_slider, duration_slider))

    def get_sound_list(self):
        sound_list = []
        for index in range(self.number_of_tones.get()):
            note = self.tones[index][0].get()
            duration = self.tones[index][1].get()

            sound_list.append(note)
            sound_list.extend((duration - 1) * [None])

        return sound_list
