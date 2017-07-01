from __future__ import print_function
from rtcmix import *
import math
import random
from datetime import datetime

"""A module containing all calls to MINC functions.

This module is an attempt to factor out calls to rtcmix functions, such
that all score scripts do not have to import the rtcmix library.
Theoretically, these functions could be re-implemented to implement the
same script in a different sound processing environment. In practice,
that would be messy unless it's an RTcmix clone.

Global contants:
    SAMPLE_RATE (int): Sample rate for the entire score.
    CHANNELS (int): Number of audio output channels for the entire score
    INSTRUMENTS (str list): Names of instruments used in this script
    REC_FORMAT (str): Audio file format to record. Options:
        aiff -- AIFF format
        aifc -- AIFC format (uncompressed)
        wav -- Microsoft RIFF (Wav) format
        next -- NeXT format (same as sun)
        sun -- Sun "au'' format (same as next)
        ircam -- IRCAM format (the older, non-hybrid BICSF format)
        raw -- raw (headerless) format
"""

global SAMPLE_RATE
global CHANNELS
global INSTRUMENTS
global REC_FORMAT
SAMPLE_RATE = 44100
CHANNELS = 2
INSTRUMENTS = [
    "WAVETABLE",
    "FMINST"
]
REC_FORMAT = "wav"

def preamble(record=False, name=""):
    """Initialize things that would go at the top of a scorefile.

    Args:
        record (bool): Whether or not to record this piece. Default False
        name (str): Name for output file, to be placed before the timestamp.
    """

    rtsetparams(SAMPLE_RATE, CHANNELS)
    load_instruments()
    control_rate(SAMPLE_RATE)
    print_off()

    name = rec_name(name)
    if record:
            rtoutput(name, REC_FORMAT)
    # RTcmix doesn't like prompts for input, or else this would work
    #else:  # Caller did not specify whether or not to record
    #    if raw_input("Record this? (y/n)  ")[0].lower()=='y':
    #        rtoutput(name, REC_FORMAT)


def load_instruments():
    """Import the Minc instruments to be used."""
    for i in INSTRUMENTS:
        load(i)

def rec_name(prefix):
    """Gets a unique name for the recording to avoid name clashes.

    Args:
        prefix (str): The prefix to the timestamp
    Returns:
        str: The unique name
    """
    name = prefix if prefix=="" else prefix+" "
    n = datetime.now()
    d = [str(n.year), str(n.month), str(n.day)]
    t = [str(n.hour), str(n.minute), str(n.second)]
    date = "-".join(d)
    time = ":".join(t)
    return name + date + "--" + time + "." + REC_FORMAT

def play(start, melody, tempo, amp, env=1, type="sine"):
    """Plays a melody using WAVETABLE.
    Todo: Decide if there should be different plays for different things or if
        everything should evaluate to a melody play call.
    """
    wave = maketable("wave", 5000, type)
    beat_dur = 60.0/tempo
    sb_per = len(melody.meter)/melody.meter.beats
    sb_dur = beat_dur/sb_per

    for i in range(len(melody)):
        dur = sb_dur * melody.rhythm.sequence[i]
        pitch = cpsmidi(melody.pitches.sequence[i])
        WAVETABLE(start, dur, amp*env, pitch, .5, wave)
        start += dur

    return start

def hold_first_beat(start, melody, tempo, amp, beats, env=1, type="sine"):
    beat_dur = 60.0/tempo
    dur = beat_dur*beats
    WAVETABLE(start, dur, amp*env, cpsmidi(melody.pitches.sequence[0]), .5, type)


def adsr(prop=[1,1,6,3,1], val=[.9,.6,.6,0] ):
    """Gets an ADSR envelope.
    Args:
        prop (list): A 5-item list representing relative length of the
            4 sections, plus a 5th silence section
        val (list): A 4-item list representing the value after each
            section. [1] and [2] should match for sustain to sustain
    """
    if len(prop) is not len(val)+1:
        raise ValueError("Lists do not match.")
    if len(prop) is not 5 or len(val) is not 4:
        raise ValueError("Lists are not size 4.")

    linelist = [0,0]
    for i in range(len(val)): linelist.extend([sum(prop[0:i+1]), val[i]])
    linelist.extend([sum(prop), 0])

    return maketable("line", 1000, *linelist)

def test():
    """Play a 5-second 440Hz sine wave for testing purposes."""
    WAVETABLE(0, 5, 20000, 440)
