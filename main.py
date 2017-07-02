# Make sure python knows to import modules from the current working directory.
# For an explanation of why this is necessary, see the README   # #
import sys                                                      # #
import os                                                       # #
sys.path.append(os.getcwd())                                    # #

import random
from util.Minc import *
from util.PitchSequence import *
from util.RhythmSequence import *
from util.Melody import *
from util.Meter import *
import config

# Preamble for RTcmix # # # # # # # # # # # # # # # # # # # # # # #
preamble(True)                                                  # #

# NOTE: This is one-measure phrases, always. Might be best to make melodies out of multple less busy measures.
def get_melody(notes, meter, scale, rstyle, rmax, mmin, mmax, mline, r=None):
    """Gets a melody fitting the parameters"""
    if mline:
        mstyle = "tri"
    else:
        mstyle = "rand"

    if r is None:
        r = RhythmSequence()
        r.gen_from_meter(meter, notes, config.fuzz, rstyle, rmax)
    p = PitchSequence()
    p.gen_from_scale(notes, scale, mline, mstyle, mmin, mmax)
    return Melody(p, r, meter)

def getA():
    tonic = config.tonic
    scale_type = config.scale
    beat_scheme = config.mbeats[config.beat]
    divisions = config.mdivs[config.div]
    meter = Meter(beat_scheme, divisions)
    bass_meter = Meter(config.mbeats[config.bass_beat], divisions)
    scale = Scale(tonic, scale_type)

    mnotes = [len(meter)/2, 3*len(meter)/5, len(meter)/5, 2*len(meter)/5, len(meter)-5]
    mmini = [tonic + 12*5 - 2, tonic + 12*5 + 3, tonic + 12*6 - 5, tonic + 12*6 + 7, tonic + 12*6 - 2]
    mmaxi = [tonic + 12*6 + 7, tonic + 12*7 + 6, tonic + 12*7 + 10, tonic + 12*8 + 6, tonic+ 12*8 + 7]
    mrmax = len(meter)/len(beat_scheme)

    bknotes = len(meter)/4
    bkmini = [tonic + 12*4 - 2, tonic + 12*4 +5, tonic + 12*5 -2]
    bkmaxi = [tonic + 12*5 + 2, tonic + 12*5 + 9, tonic + 12*6 + 2]
    bkrmax = 3*len(meter)/len(beat_scheme)/2
    bklines = (get_melody(bknotes, meter, scale, "rand", bkrmax, bkmini[0], bkmaxi[0], True), get_melody(bknotes, meter, scale, "rand", bkrmax, bkmini[0], bkmaxi[0], True))

    bnotes = 2*len(meter)/3
    bmini = tonic + 12*2 - 2
    bmaxi = tonic + 12*4 + 7
    brmax = len(meter)/len(beat_scheme)

    return (
        ( # melodies (A,B, C, D, E) = 1stAB, 2ndAB, busy
            get_melody(mnotes[0], meter, scale, "rand", mrmax, mmini[0], mmaxi[0], True),
            get_melody(mnotes[1], meter, scale, "randf", mrmax, mmini[1], mmaxi[1], False),
            get_melody(mnotes[2], meter, scale, "rand", mrmax, mmini[2], mmaxi[2], True),
            get_melody(mnotes[3], meter, scale, "randf", mrmax, mmini[3], mmaxi[3],  False),
            get_melody(mnotes[4], meter, scale, "rand", mrmax, mmini[4], mmaxi[4],  True),
        ),
        ( # backgrounds (A,B)
            (
                bklines[0],
                get_melody(bknotes, meter, scale, "rand", bkrmax, bkmini[0], bkmaxi[0], True, bklines[0].rhythm),
                get_melody(bknotes, meter, scale, "rand", bkrmax, bkmini[0], bkmaxi[0], True, bklines[0].rhythm)
            ),
            (
                bklines[1],
                get_melody(bknotes, meter, scale, "rand", bkrmax, bkmini[0], bkmaxi[0], True, bklines[1].rhythm),
                get_melody(bknotes, meter, scale, "rand", bkrmax, bkmini[0], bkmaxi[0], True, bklines[1].rhythm)
            )
        ),
        ( # bassline (ostinato)
            get_melody(bnotes, bass_meter, scale, "rand", brmax, bmini, bmaxi, False)
        )
    )


# Todo: Refactor into structure of sections with melodies and roles, relative amplitudes, envs, whatever other profiles the generation of the music
a_section = getA()
env = adsr()
bg_env = adsr([3,3,3,3,1])
st = 0
tempo = config.tempo
amp = 4000
bg_amp_mult = .6
bass_amp_mult = 1.3

# Bass by itself twice (AA)
st = play(st, a_section[2], tempo, amp*bass_amp_mult*bass_amp_mult, env, "saw3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult*bass_amp_mult, env, "saw3")

# Bass + melody (AABA)
play(st, a_section[0][0], tempo, amp, env, "square3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][1], tempo, amp, env, "square3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass + bkgnds (AABA)
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass+Bkgnds+melody (AABA)
play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][1], tempo, amp, env, "square3")
play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass + bkgnds (AABA)
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass+Bkgnds+2ndmelody (AABA)
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][3], tempo, amp, env, "square3")
play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass+Bkgnds+melody (AABA)
play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][1], tempo, amp, env, "square3")
play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass by itself twice (AA)
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Everything (AABA)
play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][1], tempo, amp, env, "square3")
play(st, a_section[0][3], tempo, amp, env, "square3")
play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Everything+high busy line(AABA)
play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[0][4], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[0][4], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][1], tempo, amp, env, "square3")
play(st, a_section[0][3], tempo, amp, env, "square3")
play(st, a_section[0][4], tempo, amp, env, "square3")
play(st, a_section[1][1][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

play(st, a_section[0][0], tempo, amp, env, "square3")
play(st, a_section[0][2], tempo, amp, env, "square3")
play(st, a_section[0][4], tempo, amp, env, "square3")
play(st, a_section[1][0][0], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Everything+high busy line(AABA)
new_amp = amp - amp/5
play(st, a_section[0][0], tempo, new_amp, env, "square3")
play(st, a_section[0][2], tempo, new_amp, env, "square3")
play(st, a_section[0][4], tempo, new_amp, env, "square3")
play(st, a_section[1][0][0], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")
new_amp -= amp/5

play(st, a_section[0][0], tempo, new_amp, env, "square3")
play(st, a_section[0][2], tempo, new_amp, env, "square3")
play(st, a_section[0][4], tempo, new_amp, env, "square3")
play(st, a_section[1][0][0], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")
new_amp -= amp/5

play(st, a_section[0][1], tempo, new_amp, env, "square3")
play(st, a_section[0][3], tempo, new_amp, env, "square3")
play(st, a_section[0][4], tempo, new_amp, env, "square3")
play(st, a_section[1][1][0], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][1], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][1][2], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")
new_amp -= amp/5

play(st, a_section[0][0], tempo, new_amp, env, "square3")
play(st, a_section[0][2], tempo, new_amp, env, "square3")
play(st, a_section[0][4], tempo, new_amp, env, "square3")
play(st, a_section[1][0][0], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][1], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
play(st, a_section[1][0][2], tempo, new_amp*bg_amp_mult, bg_env, "tri10")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")

# Bass by itself twice (AA)
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")
st = play(st, a_section[2], tempo, amp*bass_amp_mult, env, "saw3")
hold_first_beat(st, a_section[2], tempo, amp*bass_amp_mult, 2, adsr([1,1,10,3,0]))


# Old idea:
#generate a random melody from a scale
#while not sorted:
###     could add chaos anywhere in the loop
#   add emphasis
#   generate backgrounds
#   play melody and backgrounds
#   one iteration of sort
#add emphasis
#play it
