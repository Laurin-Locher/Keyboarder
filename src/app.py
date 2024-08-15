import json
import customtkinter as ctk
from tkinter import Menu, filedialog
from src.panels.arpeggiator import Arpeggiator
from src.sound.synth import Synth
from src.parameters import Parameters
from src.KeyboardVisualizer import KeyboardVisualizer
from src.panels.drums import Drums
from src.midi import MidiInput
from src.widgets.slider import Slider
from panels.keyboard import Keyboard
from panels.overtone_controls import OvertoneControls
from panels.asdr_controls import Adsr_controls
from src.panels.information_panel import InformationPanel
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
DARK_COLOR = '#1a5686'
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

    def setup_synth(self):
        self.synth = Synth(window=self, keyboardVisualizer=self, update_octave=self.update_octave,
                           octave=self.octave)
        self.synth.run()

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
        self.information_display.synth_title.configure(text=self.current_parameters.title)
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
        # self.minsize(width=1300, height=800)

    def create_main_segments(self):
        self.rowconfigure((0, 1), uniform='a', weight=1)
        self.columnconfigure(0, weight=1)

        self.controls_frame = ctk.CTkFrame(self, fg_color=self.background)
        self.controls_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10)

        self.keyboard = Keyboard(self, self.synth, self)
        self.keyboard.grid(row=1, column=0, sticky='nswe', pady=10, padx=10)

    def create_control_areas(self):
        self.controls_frame.rowconfigure(0, weight=1, uniform='a')
        self.controls_frame.columnconfigure((0, 2), weight=1, uniform='a')
        self.controls_frame.columnconfigure(1, weight=2, uniform='a')

        self.information_display = InformationPanel(self.controls_frame, self.synth, self.current_parameters,
                                                    self.highlight_color, self.octave, self)

        self.left_controls = ctk.CTkFrame(self.controls_frame, fg_color=self.background)
        self.right_controls = ctk.CTkFrame(self.controls_frame, fg_color=self.background)

        self.information_display.grid(row=0, column=1, sticky='nswe')

        self.left_controls.grid(row=0, column=0, sticky='nswe', padx=10)

        self.right_controls.grid(row=0, column=2, sticky='nswe', padx=10)

    def create_controls(self):

        self.create_left_controls()
        self.create_right_controls()

    def create_left_controls(self):
        self.left_controls.rowconfigure((0, 1), uniform='a', weight=1)
        self.left_controls.columnconfigure(0, weight=1, uniform='a')

        self.overtone_controls = OvertoneControls(self.left_controls, self.background, self.set_weight)
        self.overtone_controls.grid(row=0, column=0, sticky='nswe', pady=10)

        self.adsr_controls = Adsr_controls(self.left_controls, self.current_parameters, self.background)
        self.adsr_controls.grid(row=1, column=0, sticky='nswe', pady=10)

    def create_right_controls(self):
        self.right_controls.rowconfigure(0, weight=1, uniform='a')
        self.right_controls.rowconfigure(1, weight=3, uniform='a')
        self.right_controls.rowconfigure(2, weight=7, uniform='a')
        self.right_controls.columnconfigure(0, weight=1)

        self.create_bpm_slider()
        self.create_drums_panel()
        self.create_arpeggiator()

    def update_parameters_gui(self):
        self.information_display.synth_title.configure(text=f'{self.current_bank + 1}: {self.current_parameters.title}')
        self.adsr_controls.attack.set(self.current_parameters.attack)
        self.adsr_controls.decay.set(self.current_parameters.decay)
        self.adsr_controls.sustain.set(self.current_parameters.sustain)
        self.adsr_controls.release.set(self.current_parameters.release)
        self.adsr_controls.volume.set(self.current_parameters.volume)
        self.adsr_controls.hold.set(self.current_parameters.hold)

        for index, tone in enumerate(self.overtone_controls.overtones):
            try:
                tone.set(self.current_parameters.overtones[index])
            except IndexError:
                tone.set(0)

    def create_bpm_slider(self):
        self.bpm = ctk.IntVar(value=120)
        self.bpm_label_var = ctk.StringVar(value=f'{self.bpm.get()} bpm')

        self.bpm.trace_add('write', self._set_bpm)

        bpm_frame = ctk.CTkFrame(self.right_controls, fg_color=self.background)
        bpm_label = ctk.CTkLabel(bpm_frame, textvariable=self.bpm_label_var)
        bpm_slider = Slider(bpm_frame, variable=self.bpm, orientation='horizontal', from_=40, to=240,
                            fg_color=DARK_COLOR,
                            handle_color=ACCENT_COLOR, bg_color=DISABLED_COLOR,
                            has_handle=True, slider_width=4, handle_width=15, handle_height=5)

        bpm_label.pack(side='left')
        bpm_slider.pack(side='left', expand=True, fill='x', padx=10)

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

    def key_down(self, note, is_midi_input=False):
        if not is_midi_input:
            self.keyboard.keys[note].key_down(..., call_visualizer=False)

        overtones_doubles = []
        for tone in self.overtone_controls.overtones:
            overtones_doubles.append(tone.get())

        self.current_parameters.overtones = overtones_doubles

        self.synth.start_sound(note[0], note[1],
                               self.current_parameters,
                               self.arpeggiator.get_sound_list(),
                               offset_octave=not is_midi_input
                               )

    def key_up(self, note, is_midi_input=False):
        if not is_midi_input:
            self.keyboard.keys[note].key_up(..., call_visualizer=False)
        self.synth.stop_sound(note[0], note[1], offset_octave=not is_midi_input)

    def update_octave(self, octave):
        self.octave = octave
        self.information_display.octave_label.configure(text=f'octave: {self.octave}')
