from unittest import TestCase
from models import Chord


class ChordTest(TestCase):
    
    def test_valid_chord(self):
        cmaj = Chord([0, 0, 0, 3], tuning=list('GCEA'))
        self.assertTrue(cmaj.is_valid())
        self.assertEquals('C', cmaj.root)
        self.assertEquals('', cmaj.chordtype)
        self.assertEquals([0, 0, 0, 3], cmaj.fingers)
        self.assertEquals(list('CEG'), cmaj.normnotes)
        self.assertEquals([4, 3, 5], cmaj.interval_list)
        self.assertEquals(list('GCEC'), cmaj.allnotes)

    def test_valid_chord_repr(self):
        amaj = Chord([2, 1, 0, 0], tuning=list('GCEA'))
        self.assertTrue(amaj.is_valid())
        self.assertEquals('Chord A 2100', repr(amaj))

    def test_invalid_chord(self):
        wrong_chord = Chord([1, 1, 1, 0], tuning=list('GCEA'))
        self.assertFalse(wrong_chord.is_valid())

    def test_invalid_chord_repr(self):
        wrong_chord = Chord([1, 1, 1, 0], tuning=list('GCEA'))
        self.assertFalse(wrong_chord.is_valid())
        self.assertEquals('Chord unknown chord 1110', repr(wrong_chord))
