import rtmidi as midi
import time
from threading import Thread
from src.sound.sound import midi_index_to_note


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
        ports = self.midi_in.get_ports()
        ports_dict = {k: v for (v, k) in enumerate(ports)}

        self.midi_in.open_port(ports_dict['ARIUS'])
        print(self.midi_in.is_port_open())

        thread = Thread(target=self.main_loop)
        thread.start()

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
                print(f'press {midi_index_to_note(note_index)}')
                self.app.key_down(midi_index_to_note(note_index), update_gui=False)

            elif event_index == 128:
                self.app.key_up(midi_index_to_note(note_index), update_gui=False)

