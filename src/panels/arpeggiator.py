import customtkinter as ctk


class Arpeggiator(ctk.CTkFrame):
    def __init__(self, master, bg):
        self.background = bg
        super().__init__(master, fg_color=self.background)

        self.total_number_of_tones = 16
        self.number_of_tones = ctk.IntVar(value=self.total_number_of_tones)
        self.tones = []
        self.tone_sliders = []

        self.test_slider = ctk.CTkSlider(self)

        title = ctk.CTkLabel(self, text='Arpeggiator')
        title.pack(pady=10)

        tones_frame = ctk.CTkFrame(self, fg_color=self.background)
        for index in range(self.total_number_of_tones):
            tone = ctk.IntVar()
            duration = ctk.IntVar()
            self.tones.append((tone, duration))

            sliders = self.slider(tones_frame, f'{index + 1}', tone, duration)

            sliders.pack(expand=True, fill='y', side='left')

        tones_frame.pack(expand=True, fill='both')

        number_of_tones_slider = ctk.CTkSlider(self, orientation='horizontal', variable=self.number_of_tones, from_=0,
                                               to=self.total_number_of_tones,
                                               number_of_steps=self.total_number_of_tones + 1)
        number_of_tones_slider.pack(fill='x', padx=7)

        self.number_of_tones.trace_add('write', self.update_sliders)

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
        from src.app import ACCENT_COLOR, DISABLED_COLOR
        for index, sliders in enumerate(self.tone_sliders):
            for slider in sliders:
                if index >= self.number_of_tones.get():
                    slider.configure(fg_color=DISABLED_COLOR,
                                     button_color=DISABLED_COLOR,
                                     progress_color=DISABLED_COLOR,
                                     state='disabled')

                else:
                    slider.configure(fg_color=self.test_slider.cget('fg_color'),
                                     button_color=ACCENT_COLOR,
                                     progress_color=self.test_slider.cget('progress_color'),
                                     state='normal')

    def slider(self, master, title: str, tone, duration):
        frame = ctk.CTkFrame(master, fg_color=self.background, width=20)
        tone_slider = ctk.CTkSlider(frame, orientation='vertical', variable=tone, from_=-12, to=12, number_of_steps=24)
        duration_slider = ctk.CTkSlider(frame, orientation='vertical', variable=duration, from_=1, to=4,
                                        number_of_steps=3)
        title_label = ctk.CTkLabel(frame, text=title)

        tone_slider.place(relx=0.5, rely=0, relheight=.7, anchor='n')
        duration_slider.place(relx=0.5, rely=.7, relheight=.2, anchor='n')
        title_label.place(relx=0.5, rely=1, relheight=.1, relwidth=1, anchor='s')

        self.tone_sliders.append((tone_slider, duration_slider))

        return frame

    def get_sound_list(self):
        sound_list = []
        for index in range(self.number_of_tones.get()):
            note = self.tones[index][0].get()
            duration = self.tones[index][1].get()

            sound_list.append(note)
            sound_list.extend((duration - 1) * [None])

        return sound_list
