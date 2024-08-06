from unittest import TestCase
from sound import NOTES, transpose


class SoundTest(TestCase):

    def test_transpose(self):
        self.assertEqual(transpose('C', 1, 0), ('C', 1))
        self.assertEqual(transpose('C', 1, 1), ('C#', 1))
        self.assertEqual(transpose('C', 1, -1), ('B', 1))
        self.assertEqual(transpose('C', 1, 12), ('C', 2))
        self.assertEqual(transpose('C', 1, -12), ('C', 0))

