import rtmidi as midi
import time
from threading import Thread
from src.sound.sound import midi_index_to_note
from src.selectinput import SelectInput


# out = rtmidi.MidiOut()
#
# ports = out.get_ports()
# ports_dict = {k: v for (v, k) in enumerate(ports)}
#
# print(ports_dict)
# out.open_port(ports_dict['ARIUS'])
#
# with out:
#     note_on = [0x94, 48, 100]
#     note_off = [0x84, 48, 0]
#
#     out.send_message(note_on)
#     time.sleep(1.0)
#     out.send_message(note_off)

class MidiInput:
    def __init__(self, app):
        self.app = app

        self.midi_in = midi.MidiIn()

        self.last_ports = []
        self.current_port = None
        thread = Thread(target=self.check_for_new_input)
        thread.start()

        thread = Thread(target=self.main_loop)
        thread.start()

    def check_for_new_input(self):
        ports = self.midi_in.get_ports()

        if not ports:
            ports = []

        if not ports == self.last_ports:
            print('inputs changed')
            if len(ports) > len(self.last_ports):
                self.ports_dict = {k: v for (v, k) in enumerate(ports)}
                SelectInput(ports, self.open_port)

            else:
                self.close_port()

        self.last_ports = ports.copy()
        time.sleep(1)
        self.check_for_new_input()

    def open_port(self, port):
        try:
            self.current_port = port
            self.midi_in.open_port(self.ports_dict[self.current_port])

        except KeyError:
            self.close_port()

    def close_port(self):
        self.midi_in.close_port()
        self.current_port = None

    def main_loop(self):
        while True:
            message_and_duration = self.midi_in.get_message()

            try:
                message, duration = message_and_duration

            except TypeError:
                time.sleep(0.001)
                continue

            event_index = message[0]
            note_index = message[1]

            if event_index == 144:
                note, octave = midi_index_to_note(note_index)
                self.app.key_down(midi_index_to_note(note_index), is_midi_input=True)

            elif event_index == 128:
                self.app.key_up(midi_index_to_note(note_index), is_midi_input=True)
