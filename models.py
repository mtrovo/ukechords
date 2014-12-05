import pymongo
from pymongo.mongo_client import MongoClient
client = MongoClient()
db = client.ukulele

Tuning = ['G', 'C', 'E', 'A']
Pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SortPitches = sorted(Pitches)


class Chord(object):
    
    def __init__(self, fingers, tuning=Tuning):
        self.fingers = fingers
        self.tuning = tuning
        
        self.allnotes = [Pitches[(Pitches.index(tone) + f) % 12]
                         for f, tone in zip(fingers, tuning)]
        
        ##normalize
        self.normnotes = list(set(self.allnotes))
        self.normnotes.sort()

        ##intervals
        N = len(self.normnotes)
        pitchlist = [SortPitches.index(note) for note in self.normnotes]
        self.interval_list = [None] * N
        for i in range(N):
            delta = pitchlist[(i + 1) % N] - pitchlist[i]
            self.interval_list[i] = delta if delta >= 0 else delta + 12
            
        #decode
        self.chordtype = None
        self.root = None
        self.valid = False

        for i in range(len(self.interval_list)):
            if self.interval_list == [3, 4, 5]:
                self.chordtype = "m"
            elif self.interval_list == [4, 3, 5]:
                self.chordtype = ""
            elif self.interval_list == [4, 3, 3, 2]:
                self.chordtype = "7"
            elif self.interval_list == [4, 3, 4, 1]:
                self.chordtype = "maj7"
            elif self.interval_list == [3, 4, 3, 2]:
                self.chordtype = "m7"
            elif self.interval_list == [3, 3, 6]:
                self.chordtype = "dim"
            elif self.interval_list == [4, 4, 4]:
                self.chordtype = "aug"
            elif self.interval_list == [2, 2, 3, 5]:
                self.chordtype = "9"
            elif self.interval_list == [5, 2, 5]:
                self.chordtype = "sus"
            elif self.interval_list == [7, 5]:
                self.chordtype = "5"
            elif self.interval_list == [3, 3, 3, 3]:
                self.chordtype = "dim7"
            elif self.interval_list == [3, 3, 4, 2]:
                self.chordtype = "m7b5"
            # C6 = Am7, etc., so we never mention 6th chords.
            
            if self.chordtype is not None:
                self.root = self.normnotes[0]
                self.valid = True
                break

            # rotate lists
            self.interval_list.append(self.interval_list.pop(0))
            self.normnotes.append(self.normnotes.pop(0))

    def is_valid(self):
        return self.chordtype is not None

    def __str__(self):
        ret = ['Chord']
        if not self.is_valid():
            ret.append('unknown chord')
        else:
            ret.append(self.root + self.chordtype)

        ret.append(self.fingers_str())
        return ' '.join(ret)

    def fingers_str(self):
        return ''.join(map(str, self.fingers))

    def fullname(self):
        return self.root + self.chordtype
        
    def __repr__(self):
        return str(self)

    def to_dict(self):
        return dict(
            root=self.root,
            fingers=self.fingers,
            tuning=self.tuning,
            allnotes=self.allnotes,
            normnotes=self.normnotes,
            fullname=self.fullname(),
            inteval_list=self.interval_list,
            chordtype=self.chordtype
        )


def save_chord(chord):
    if not chord.is_valid():
        raise Exception('not a valid chord')

    kv = chord.to_dict()
    kv['fingers_str'] = chord.fingers_str()
    kv['fings_sum'] = sum(chord.fingers)
    kv['fings_min'] = min(chord.fingers)
    kv['_id'] = dict(tuning=kv.pop('tuning'),
                     fings=kv.pop('fingers'))

    db.chords.save(kv)


def find_chordtypes_by_note():
    return db.chords.aggregate({'$group': {'_id': '$root', 'types':
                               {'$addToSet': '$fullname'}}},
                               {'$sort': {'_id': 1}})


def get_chords_by_fullname(fullname):
    return db.chords.find({'fullname': fullname}) \
             .sort('fings_sum', pymongo.ASCENDING)


def get_all_first_chord():
    group = {'$group': {'_id': '$fullname',
             'root': {'$first': '$root'},
             'first': {'$first': '$_id'}}}
    result = db.chords.aggregate([{'$sort': dict(fings_min=1, fings_sum=1)},
                                  group,
                                  {'$sort': dict(root=1, _id=1)}])

    return [Chord(c['first']['fings'], c['first']['tuning'])
            for c in result['result']]
