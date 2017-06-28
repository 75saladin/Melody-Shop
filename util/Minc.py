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

def preamble(record=False):
    """Initialize things that would go at the top of a scorefile.

    Args:
        record (bool): Whether or not to record this piece. Default False
    """

    rtsetparams(SAMPLE_RATE, CHANNELS)
    load_instruments()
    print_off()

    name = rec_name()
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

def rec_name():
    """Gets a unique name for the recording to avoid name clashes.

    Returns:
        str: The unique name
    """
    name = ""
    n = datetime.now()
    d = [str(n.year), str(n.month), str(n.day)]
    t = [str(n.hour), str(n.minute), str(n.second)]
    date = "-".join(d)
    time = ":".join(t)
    return name + date + "--" + time + "." + REC_FORMAT

def play(start, melody, tempo, amp, env=1, type="sine"):
    """Plays a melody using WAVETABLE."""
    beat_dur = 60.0/tempo
    sb_per = len(melody.meter)/melody.meter.beats
    sb_dur = beat_dur/sb_per

    for i in range(len(melody)):
        dur = sb_dur * melody.rhythm.sequence[i]
        pitch = cpsmidi(melody.pitches.sequence[i])
        WAVETABLE(start, dur, amp*env, pitch, .5, type)
        start += dur

    return start

def hold_first_beat(start, melody, tempo, amp, beats, env=1, type="sine"):
    beat_dur = 60.0/tempo
    dur = beat_dur*beats
    WAVETABLE(start, dur, amp*env, cpsmidi(melody.pitches.sequence[0]), .5, type)


def adsr(prop=[1,1,6,3,1], val=[1,.6,.6,0] ):
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
    return maketable(
        "line", 50*sum(prop), 0,0, prop[0], val[0], prop[0]+prop[1], val[1],
        prop[0]+prop[1]+prop[2], val[2], prop[0]+prop[1]+prop[2]+prop[3],
        val[3], sum(prop), 0)

def test():
    """Play a 5-second 440Hz sine wave for testing purposes."""
    WAVETABLE(0, 5, 20000, 440)
