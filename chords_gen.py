import models
from itertools import product, groupby


def print_chords_table(chords):
    chords.sort(lambda a, b: cmp(a.root, b.root))
    for root, cs in groupby(chords, lambda x: x.root):
        print "#", root
        cs = sorted(cs, lambda a, b: cmp(a.chordtype, b.chordtype))
        it = iter(cs)
        for csrow in zip(*[it] * 4):
            print ' '.join(map(lambda c: "%20s" % repr(c), csrow))


def main(tuning='GCEA', is_dryrun=False, **kvargs):
    tuning = list(tuning)
    minfret = 0
    maxfret = 10
    maxwindow = 5

    chords = []
    for fingers in product(range(minfret, maxwindow), repeat=4):
        chord = models.Chord(fingers)
        if chord.is_valid():
            chords.append(chord)

    for i in xrange(minfret + 1, maxfret - maxwindow):
        
        for fingers in product(range(i, i + maxwindow), repeat=4):
            if max(fingers) == maxwindow + i - 1:
                chord = models.Chord(fingers)
                if chord.is_valid():
                    chords.append(chord)

    if is_dryrun:
        print_chords_table(chords)
    else:
        for chord in chords:
            print 'saving chord', repr(chord)
            models.save_chord(chord)


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-t", "--tuning", dest="tuning",
                      default="GCEA",
                      help="ukulele chords tuning from upper to lower")
    parser.add_option("-d", "--dry-run", dest="is_dryrun",
                      default=False, action='store_true')

    options, args = parser.parse_args()
    main(vars(options))
