import models
from itertools import product, groupby


def main():
    minfret = 0
    maxfret = 10
    maxwindow = 5

    chords = []
    for fingers in product(range(maxwindow), repeat=4):
        chord = models.Chord(fingers)
        if chord.is_valid():
            chords.append(chord)

    for i in xrange(1, maxfret - maxwindow):
        
        for fingers in product(range(i, i + maxwindow), repeat=4):
            if max(fingers) == maxwindow + i - 1:
                chord = models.Chord(fingers)
                if chord.is_valid():
                    chords.append(chord)

    chords.sort(lambda a, b: cmp(a.root, b.root))
    for root, cs in groupby(chords, lambda x: x.root):
        print "#", root
        cs = sorted(cs, lambda a, b: cmp(a.chordtype, b.chordtype))
        it = iter(cs)
        for csrow in zip(*[it] * 4):
            print ' '.join(map(lambda c: "%20s" % repr(c), csrow))

    #for ini in xrange(minfret + 1, maxfret - maxwindow):




if __name__ == '__main__':
    main()