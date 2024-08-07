from unittest import TestCase
from sound import NOTES, transpose, midi_index_to_note


class SoundTest(TestCase):

    def test_transpose(self):
        self.assertEqual(transpose('C', 1, 0), ('C', 1))
        self.assertEqual(transpose('C', 1, 1), ('C#', 1))
        self.assertEqual(transpose('C', 1, -1), ('B', 1))
        self.assertEqual(transpose('C', 1, 12), ('C', 2))
        self.assertEqual(transpose('C', 1, -12), ('C', 0))

    def test_index_to_note(self):
        self.assertEqual(midi_index_to_note(21), ('A', 0))
        self.assertEqual(midi_index_to_note(22), ('A#', 0))
        self.assertEqual(midi_index_to_note(25), ('C#', 0))
        self.assertEqual(midi_index_to_note(71), ('B', 4))
        self.assertEqual(midi_index_to_note(108), ('C', 7))


