import customtkinter as ctk
from src.widgets.round_slider import RoundSlider


class Adsr_controls(ctk.CTkFrame):
    def __init__(self, master, current_parameters, background, app):
        self.current_parameters = current_parameters
        self.app = app
        self.background = background

        super().__init__(master, fg_color=self.background)

        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')

        self.attack = ctk.DoubleVar(value=self.current_parameters.attack)
        self.attack_str = ctk.StringVar(value='')
        self.attack.trace_add('write', self._set_attack)
        self._set_attack()

        self.slider(self, 'Attack', self.attack, self.attack_str, 0.01, 1, 0, 0)

        self.decay = ctk.DoubleVar(value=self.current_parameters.decay)
        self.decay_str = ctk.StringVar(value='')
        self.decay.trace_add('write', self._set_decay)
        self._set_decay()

        self.slider(self, 'Decay', self.decay, self.decay_str, 0.01, 1, 0, 1)

        self.sustain = ctk.DoubleVar(value=self.current_parameters.sustain)
        self.sustain_str = ctk.StringVar(value='')
        self.sustain.trace_add('write', self._set_sustain)
        self._set_sustain()

        self.slider(self, 'Sustain', self.sustain, self.sustain_str, 0, 1, 0, 2)

        self.release = ctk.DoubleVar(value=self.current_parameters.release)
        self.release_str = ctk.StringVar(value='')
        self.release.trace_add('write', self._set_release)
        self._set_release()

        self.slider(self, 'Release', self.release, self.release_str, 0, 1, 0, 3)

        self.volume = ctk.DoubleVar(value=self.current_parameters.volume)
        self.volume_str = ctk.StringVar(value='')
        self.volume.trace_add('write', self._set_volume)
        self._set_volume()

        self.slider(self, 'Volume', self.volume, self.volume_str, 0, 10, 0, 4)

        self.hold = ctk.BooleanVar(value=True)
        self.checkbox = ctk.CTkCheckBox(self, text='Hold', variable=self.hold, bg_color=self.background)
        self.hold.trace_add('write', self.set_hold)

        self.checkbox.grid(row=0, column=5, sticky='ns', rowspan=3)

        # self.bind('<Configure>', lambda _: self.re_grid_everything())

    def set_hold(self, *args):
        self.app.current_parameters.hold = self.hold.get()

    def slider(self, master, title: str, var, str_var, from_, to, row, column):
        from src.app import ACCENT_COLOR
        slider = RoundSlider(self, variable=var, from_=from_, to=to, canvas_bg_color=self.background, fg_color='#fff',
                             highlight_color=ACCENT_COLOR, max_size=110)

        text_frame = ctk.CTkFrame(self, fg_color=self.background)
        title_label = ctk.CTkLabel(text_frame, text=title)
        amount = ctk.CTkLabel(text_frame, textvariable=str_var)

        slider.grid(row=row, column=column, sticky='nswe', pady=10, padx=10)

        title_label.pack(fill='x')
        amount.pack(fill='x')

        text_frame.grid(row=row+1, column=column, sticky='n', pady=5)

    def _set_attack(self, *args):
        value = self.attack.get()
        self.app.current_parameters.attack = value
        self.attack_str.set(f'{value:.2f}')

    def _set_decay(self, *args):
        value = self.decay.get()
        self.app.current_parameters.decay = value

        self.decay_str.set(f'{value:.2f}')

    def _set_sustain(self, *args):
        value = self.sustain.get()
        self.app.current_parameters.sustain = value

        self.sustain_str.set(f'{value:.2f}')

    def _set_release(self, *args):
        value = self.release.get()
        self.app.current_parameters.release = value
        self.release_str.set(f'{value:.2f}')

    def _set_volume(self, *args):
        value = self.volume.get()
        self.app.current_parameters.volume = value

        self.volume_str.set(f'{value:.2f}')
