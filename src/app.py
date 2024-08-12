import json

import customtkinter as ctk
from PIL import Image
from tkinter import Menu, filedialog
from src.panels.arpeggiator import Arpeggiator
from src.sound.synth import Synth
from src.widgets.key import Key
from src.parameters import Parameters
from src.KeyboardVisualizer import KeyboardVisualizer
from widgets.imagebutton import ImageButton
from src.panels.drums import Drums
from src.midi import MidiInput
from src.widgets.round_slider import RoundSlider


# KEY_BINDING = {
#     'a': ('B', 0),
#     's': ('C', 0),
#     'e': ('C#', 0),
#     'd': ('D', 0),
#     'r': ('D#', 0),
#     'f': ('E', 0),
#     'g': ('F', 0),
#     'z': ('F#', 0),
#     'h': ('G', 0),
#     'u': ('G#', 0),
#     'j': ('A', 1),
#     'i': ('A#', 1),
#     'k': ('B', 1),
#     'l': ('C', 1),
#     'p': ('C#', 1),
#     'ö': ('D', 1),
#     'ü': ('D#', 1),
#     'ä': ('E', 1),
#     '$': ('F', 1)
# }

ACCENT_COLOR = '#206aa5'
DISABLED_COLOR = '#383838'


class App(ctk.CTk, KeyboardVisualizer):
    def __init__(self):
        self.background = '#000'
        self.highlight_color = '#222'

        super().__init__(fg_color=self.background)

        # Window config
        self.configure_window()

        self.octave = 2
        self.current_parameters = Parameters()

        # Synth
        self.setup_synth()

        # Menu
        self.create_menu()

        # Widgets & Layout
        self.create_gui()

        # parameters
        self.setup_parameters()

        # Midi Input
        MidiInput(self)

        # Mainloop
        self.mainloop()

    def create_gui(self):
        self.create_main_segments()
        self.create_control_areas()
        self.create_controls()
        self.fill_information_frame()
        self.create_keys()

    def setup_synth(self):
        self.synth = Synth(window=self, keyboardVisualizer=self, update_octave=self.update_octave, octave=self.octave)
        self.synth.run()

    def create_main_segments(self):
        self.rowconfigure((0, 1), uniform='a', weight=1)
        self.columnconfigure(0, weight=1)

        self.keyboard_frame = ctk.CTkFrame(self, fg_color=self.background)
        self.keyboard_frame.grid(row=1, column=0, sticky='nswe', pady=10, padx=10)
        self.controls_frame = ctk.CTkFrame(self, fg_color=self.background)
        self.controls_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10)

    def create_menu(self):
        self.menu = Menu(self)
        self.configure(menu=self.menu)
        self.file_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.file_menu)

        self.file_menu.add_command(label='Load Parameters', command=self.load_parameters)
        self.file_menu.add_command(label='Rename Parameters', command=self.rename_parameters)
        self.file_menu.add_command(label='Save parameters', command=self.save_parameter)
        self.file_menu.add_command(label='Save parameters set', command=self.save_all_parameters)

        self.file_menu.add_separator()

        self.file_menu.add_command(label='Load Drum', command=self.load_drum)
        self.file_menu.add_command(label='Save Drum', command=self.save_drum)

        self.file_menu.add_separator()

        self.file_menu.add_command(label='Load Arpeggiator', command=self.load_arpeggiator)
        self.file_menu.add_command(label='Save Arpeggiator', command=self.save_arpeggiator)

    def save_all_parameters(self):
        Parameters.save_all_parameters(self.all_parameters)

    def save_parameter(self):
        path = filedialog.asksaveasfilename(
            title='Save parameters',
            initialdir='resource/files/parameters'
        )

        if len(path) > 0:
            with open(path, 'w') as f:
                json.dump(self.current_parameters.to_dict(), f)

    def rename_parameters(self):
        self.current_parameters.title = ctk.CTkInputDialog(text='Rename parameters', title='Rename').get_input()
        self.synth_title.configure(text=self.current_parameters.title)
        self.update_parameters_gui()

    def load_parameters(self):
        path = filedialog.askopenfilename(
            title='Select parameter file',
            initialdir='resource/files/parameters',
        )

        if len(path) > 0:
            with open(path, 'r') as f:
                self.current_parameters.from_dict(json.load(f))

            self.update_parameters_gui()

    def save_drum(self):
        path = filedialog.asksaveasfilename(
            title='Save drum',
            initialdir='resource/files/drums'
        )

        if len(path) > 0:
            with open(path, 'w') as f:
                json.dump(self.drums.to_dict(), f)

    def load_drum(self):
        path = filedialog.askopenfilename(
            title='Select parameter file',
            initialdir='resource/files/drums',
        )

        if len(path) > 0:
            with open(path, 'r') as f:
                self.drums.from_dict(json.load(f))

    def save_arpeggiator(self):
        path = filedialog.asksaveasfilename(
            title='Save arpeggiator',
            initialdir='resource/files/arpeggiator'
        )

        if len(path) > 0:
            with open(path, 'w') as f:
                json.dump(self.arpeggiator.to_dict(), f)

    def load_arpeggiator(self):
        path = filedialog.askopenfilename(
            title='Select arpeggiator file',
            initialdir='resource/files/arpeggiator',
        )

        if len(path) > 0:
            with open(path, 'r') as f:
                self.arpeggiator.from_dict(json.load(f))

    def configure_window(self):
        self.title('Keyboarder')
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')
        # self.geometry(f'{1300}x{800}')
        self.minsize(width=1300, height=800)

    def setup_parameters(self):
        try:
            self.all_parameters = Parameters.load_all_parameters()
        except FileNotFoundError:
            self.all_parameters = []

        while len(self.all_parameters) < 10:
            self.all_parameters.append(Parameters())
        self.set_current_bank(0)
        for bank in range(10):
            self.bind(f'<KeyPress-{(bank + 1) % 10}>', lambda _, i=bank: self.set_current_bank(i))

    def set_current_bank(self, index):
        self.current_bank = index
        self.current_parameters = self.all_parameters[index]
        self.update_parameters_gui()

    def update_parameters_gui(self):
        self.synth_title.configure(text=f'{self.current_bank + 1}: {self.current_parameters.title}')
        self.attack.set(self.current_parameters.attack)
        self.decay.set(self.current_parameters.decay)
        self.sustain.set(self.current_parameters.sustain)
        self.release.set(self.current_parameters.release)
        self.volume.set(self.current_parameters.volume)
        self.hold.set(self.current_parameters.hold)

        for index, tone in enumerate(self.overtones):
            try:
                tone.set(self.current_parameters.overtones[index])
            except IndexError:
                tone.set(0)

    def fill_information_frame(self):
        self.synth_title = ctk.CTkLabel(self.information_display, text=self.current_parameters.title,
                                        font=('Arial', 60))
        self.synth_title.place(relx=0.5, rely=0.01, anchor='n', relheight=0.2, relwidth=1)
        octave_changer = self.create_octave_changer()

        padding = 0.01
        octave_changer.place(relx=0 + padding, rely=1 - padding, anchor='sw', relwidth=0.3, relheight=.1)

        ui_scale = ctk.DoubleVar(value=1)
        ui_scale.trace_add('write', lambda _, __, ___: ctk.set_widget_scaling(ui_scale.get()))

        ui_scaler = ctk.CTkSlider(self.information_display, variable=ui_scale, from_=0, to=2)
        ui_scaler.place(relx=0.95, rely=.95, relwidth=.69, anchor='se')

        self.create_graph()

    def create_graph(self):
        self.graph = ctk.CTkCanvas(self.information_display, bg='#444', highlightthickness=0)
        self.graph.place(relx=0.5, rely=0.22, relheight=0.6, relwidth=0.98, anchor='n')
        self.graph.update()
        self.draw_graph()

    def draw_graph(self):
        self.graph.delete('all')
        buffer = self.synth.get_buffer()
        width = self.graph.winfo_width()
        factor_x = width / len(buffer)
        height = self.graph.winfo_height()
        x0 = y0 = None
        for i in range(len(buffer)):
            x1 = int(i * factor_x)
            y1 = int(.5 * height + .45 * height * buffer[i])
            if x0 is not None:
                self.graph.create_line(x0, y0, x1, y1, fill='white')
            x0 = x1
            y0 = y1
        self.after(10, self.draw_graph)

    def create_controls(self):

        self.create_left_controls()
        self.create_right_controls()

    def create_left_controls(self):
        self.left_controls.rowconfigure((0, 1), uniform='a', weight=1)
        self.left_controls.columnconfigure(0, weight=1)

        self.create_overtone_controls()
        self.create_adsr_controls()

    def create_right_controls(self):
        self.right_controls.rowconfigure(0, weight=1, uniform='a')
        self.right_controls.rowconfigure(1, weight=3, uniform='a')
        self.right_controls.rowconfigure(2, weight=7, uniform='a')
        self.right_controls.columnconfigure(0, weight=1)

        self.create_bpm_slider()
        self.create_drums_panel()
        self.create_arpeggiator()

    def create_bpm_slider(self):
        self.bpm = ctk.IntVar(value=120)
        self.bpm_label_var = ctk.StringVar(value=f'{self.bpm.get()} bpm')

        self.bpm.trace_add('write', self._set_bpm)

        bpm_frame = ctk.CTkFrame(self.right_controls, fg_color=self.background)
        bpm_label = ctk.CTkLabel(bpm_frame, textvariable=self.bpm_label_var)
        bpm_slider = ctk.CTkSlider(bpm_frame, variable=self.bpm, orientation='horizontal', from_=40, to=240)

        bpm_label.pack(side='left')
        bpm_slider.pack(side='left', expand=True, fill='x')

        bpm_frame.grid(row=0, column=0, sticky='nswe', pady=10)

    def _set_bpm(self, *args):
        self.bpm_label_var.set(f'{self.bpm.get()} bpm')
        self.synth.set_bpm(self.bpm.get())

    def create_drums_panel(self):
        self.drums = Drums(self.right_controls, self.background, self.synth, self.bpm)
        self.drums.grid(row=1, column=0, sticky='nswe', pady=10)
        self.synth.add_tick_subscriber(self.drums)

    def create_arpeggiator(self):
        self.arpeggiator = Arpeggiator(self.right_controls, self.background)
        self.arpeggiator.grid(row=2, column=0, sticky='nswe', pady=10)

    def set_weight(self, index, value):
        self.current_parameters.overtones[index] = value.get()

    def create_overtone_controls(self):
        self.overtone_controls = ctk.CTkFrame(self.left_controls, fg_color=self.background)
        self.overtone_controls.grid(row=0, column=0, sticky='nswe', pady=10)

        bar = ctk.CTkFrame(self.overtone_controls, fg_color=self.background)
        label = ctk.CTkLabel(bar, text='Overtones', font=('Arial', 15))
        label.pack(side='top', padx=10)

        def reset():
            value = 1
            for weight_ in self.overtones:
                weight_.set(value=value)
                value = 0

        reset = ctk.CTkButton(bar, text='Reset', fg_color=self.background,
                              hover_color=self.background,
                              command=reset)
        reset.pack(side='right', padx=10)
        bar.pack()
        number_of_controls = 15
        self.overtones = []
        default = 1
        for index in range(number_of_controls):
            weight = ctk.DoubleVar(value=default)
            slider = ctk.CTkSlider(self.overtone_controls, orientation='vertical', variable=weight)
            slider.pack(side='left', expand=True, fill='y')

            self.overtones.append(weight)

            weight.trace_add('write', callback=lambda _, __, ___, i=index, w=weight: self.set_weight(i, w))

            default = 0

    def create_adsr_controls(self):
        self.adsr_controls = ctk.CTkFrame(self.left_controls, fg_color=self.background)
        self.adsr_controls.grid(row=1, column=0, sticky='nswe', pady=10)

        self.attack = ctk.DoubleVar(value=self.current_parameters.attack)
        self.attack_str = ctk.StringVar(value='')
        self.attack.trace_add('write', self._set_attack)
        self._set_attack()

        attack_slider = self.slider(self.adsr_controls, 'Attack', self.attack, self.attack_str, 0.01, 1)

        self.decay = ctk.DoubleVar(value=self.current_parameters.decay)
        self.decay_str = ctk.StringVar(value='')
        self.decay.trace_add('write', self._set_decay)
        self._set_decay()

        decay_slider = self.slider(self.adsr_controls, 'Decay', self.decay, self.decay_str, 0.01, 1)

        self.sustain = ctk.DoubleVar(value=self.current_parameters.sustain)
        self.sustain_str = ctk.StringVar(value='')
        self.sustain.trace_add('write', self._set_sustain)
        self._set_sustain()

        sustain_slider = self.slider(self.adsr_controls, 'Sustain', self.sustain, self.sustain_str, 0, 1)

        self.release = ctk.DoubleVar(value=self.current_parameters.release)
        self.release_str = ctk.StringVar(value='')
        self.release.trace_add('write', self._set_release)
        self._set_release()

        release_slider = self.slider(self.adsr_controls, 'Release', self.release, self.release_str, 0, 1)

        self.volume = ctk.DoubleVar(value=self.current_parameters.volume)
        self.volume_str = ctk.StringVar(value='')
        self.volume.trace_add('write', self._set_volume)
        self._set_volume()

        volume_slider = self.slider(self.adsr_controls, 'Volume', self.volume, self.volume_str, 0, 10)

        self.hold = ctk.BooleanVar(value=True)
        checkbox = ctk.CTkCheckBox(self.adsr_controls, text='Hold', variable=self.hold)
        self.hold.trace_add('write', self.set_hold)

        self.adsr_controls.rowconfigure((0, 1), weight=1, uniform='a')
        self.adsr_controls.columnconfigure((0, 1, 2), weight=1, uniform='a')

        attack_slider.grid(row=0, column=0, sticky='nswe')
        decay_slider.grid(row=0, column=1, sticky='nswe')
        sustain_slider.grid(row=0, column=2, sticky='nswe')
        release_slider.grid(row=1, column=0, sticky='nswe')
        volume_slider.grid(row=1, column=1, sticky='nswe')
        checkbox.grid(row=1, column=2, sticky='ns')

    def set_hold(self, *args):
        self.current_parameters.hold = self.hold.get()

    def slider(self, master, title: str, var, str_var, from_, to):
        frame = ctk.CTkFrame(master, fg_color=self.background, width=50)
        slider = RoundSlider(frame, variable=var, from_=from_, to=to, canvas_bg_color=self.background)
        title_label = ctk.CTkLabel(frame, text=title)
        amount = ctk.CTkLabel(frame, textvariable=str_var)

        frame.rowconfigure(0, weight=3, uniform='a')
        frame.rowconfigure((1, 2), weight=1, uniform='a')
        slider.grid(row=0, column=0, sticky='nswe')
        title_label.grid(row=1, column=0, sticky='nswe')
        amount.grid(row=2, column=0, sticky='nswe')

        return frame

    def _set_attack(self, *args):
        value = self.attack.get()
        self.current_parameters.attack = value
        self.attack_str.set(f'{value:.2f}')

    def _set_decay(self, *args):
        value = self.decay.get()
        self.current_parameters.decay = value

        self.decay_str.set(f'{value:.2f}')

    def _set_sustain(self, *args):
        value = self.sustain.get()
        self.current_parameters.sustain = value

        self.sustain_str.set(f'{value:.2f}')

    def _set_release(self, *args):
        value = self.release.get()
        self.current_parameters.release = value
        self.release_str.set(f'{value:.2f}')

    def _set_volume(self, *args):
        value = self.volume.get()
        self.current_parameters.volume = value

        self.volume_str.set(f'{value:.2f}')

    def create_control_areas(self):
        self.controls_frame.rowconfigure(0, weight=1)
        self.controls_frame.columnconfigure((0, 2), weight=1, uniform='a')
        self.controls_frame.columnconfigure(1, weight=2, uniform='a')
        self.information_display = ctk.CTkFrame(self.controls_frame, fg_color=self.highlight_color)
        self.left_controls = ctk.CTkFrame(self.controls_frame, fg_color=self.background)
        self.right_controls = ctk.CTkFrame(self.controls_frame, fg_color=self.background)

        self.information_display.grid(row=0, column=1, sticky='nswe')

        self.left_controls.grid(row=0, column=0, sticky='nswe', padx=10)

        self.right_controls.grid(row=0, column=2, sticky='nswe', padx=10)

    def create_octave_changer(self):
        octave_frame = ctk.CTkFrame(self.information_display, fg_color=self.highlight_color)
        self.octave_label = ctk.CTkLabel(octave_frame, text=f'octave: {self.octave}', font=('Arial', 20))

        change_frame = ctk.CTkFrame(octave_frame, fg_color=self.highlight_color)
        increase = self.create_image_button(change_frame, 'increase', lambda _: self.synth.change_octave(1))
        decrease = self.create_image_button(change_frame, 'decrease', lambda _: self.synth.change_octave(-1))

        increase.pack()
        decrease.pack()
        change_frame.pack(side='left', padx=10)
        self.octave_label.pack(side='left', padx=10)

        self.bind('<KeyPress-Up>', lambda _: self.synth.change_octave(1))
        self.bind('<KeyPress-Down>', lambda _: self.synth.change_octave(-1))

        return octave_frame

    @staticmethod
    def create_image_button(master, folder, command):
        white_normal = Image.open(f'resource/symbols/{folder}/white/normal.png')
        white_pressed = Image.open(f'resource/symbols/{folder}/white/pressed.png')
        black_normal = Image.open(f'resource/symbols/{folder}/black/normal.png')
        black_pressed = Image.open(f'resource/symbols/{folder}/black/pressed.png')
        normal = ctk.CTkImage(light_image=black_normal,
                              dark_image=white_normal
                              )
        pressed = ctk.CTkImage(light_image=black_pressed,
                               dark_image=white_pressed
                               )
        increase = ImageButton(master, normal, pressed, command)
        return increase

    def update_octave(self, octave):
        self.octave = octave
        self.octave_label.configure(text=f'octave: {self.octave}')

    def create_keys(self):
        notes = []
        for binding in Synth.KEY_BINDING:
            notes.append(Synth.KEY_BINDING[binding])
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
                key = Key(self.keyboard_frame, 'white', note, self)
                key.place(relx=key_pos, rely=0, relheight=1, relwidth=rel_key_width)

                key_pos += rel_key_width

                self.keys[note] = key

            else:
                key = Key(self.keyboard_frame, 'black', note, self)
                width = rel_key_width * 0.5
                x = key_pos - rel_key_width / 4
                key.place(relx=x, rely=0, relheight=0.65, relwidth=width)
                black_keys.append(key)

                self.keys[note] = key

            for key in black_keys:
                key.lift()

    def key_down(self, note, is_midi_input=False):
        if not is_midi_input:
            self.keys[note].key_down(..., call_visualizer=False)

        overtones_doubles = []
        for tone in self.overtones:
            overtones_doubles.append(tone.get())

        self.current_parameters.overtones = overtones_doubles

        self.synth.start_sound(note[0], note[1],
                               self.current_parameters,
                               self.arpeggiator.get_sound_list(),
                               offset_octave=not is_midi_input
                               )

    def key_up(self, note, is_midi_input=False):
        if not is_midi_input:
            self.keys[note].key_up(..., call_visualizer=False)
        self.synth.stop_sound(note[0], note[1], offset_octave=not is_midi_input)
