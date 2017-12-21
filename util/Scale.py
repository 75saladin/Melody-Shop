from sets import *
import random

class Scale(object):
    """A class to represent a musical scale.

    Doesn't contain any concrete pitches. It simply describes the pitch
    classes, relative to the tonic, that are a part of this scale.

    Class constants:
        KNOWN_SCALES (dict): String keys for common scale names retrieve
            the pitch class set representing the scale

    Attributes:
        tonic (int): A midi note number representing the lowest octave of
            the root note for this scale. 0 = C, 1 = C#, and so on.
        members (int list): A set of pitch classes that are a part of
            this scale. Pitch classes are ints representing number of
            half-steps above the tonic. Tonic + pitch class = midi note
            in scale.
    """
    global KNOWN_SCALES
    KNOWN_SCALES = {
        "chrom": Set([i for i in range(12)]),
        "major": Set([0, 2, 4, 5, 7, 9, 11]),
        "whole": Set([0, 2, 4, 6, 8, 10]),
        "octwh": Set([0, 2, 3, 5, 6, 8, 9, 11]),
        "octhw": Set([0, 1, 3, 4, 6, 7, 9, 10]),
        "natmin": Set([0, 2, 3, 5, 7, 8, 10]),
        "harmin": Set([0, 2, 3, 5, 7, 8, 11]),
        "mjpent": Set([0, 2, 4, 7, 9]),
        "mnpent": Set([0, 3, 5, 7, 10]),
        "blues": Set([0, 3, 5, 6, 7, 10]),
        "gypsy": Set([0, 1, 4, 5, 7, 8, 11]),
        "qtpent": Set([0, 3.5, 5, 7, 10.5]),
        "qchrom": Set([i/2.0 for i in range(24)]),
        "microaf": Set([i/4.0 for i in range(48)]),
        # Fake scales, Todo implement general abstract note thing
        "note": Set([0]),
        "diabolus": Set([0, 6]),
        "beeth": Set([0, 7])
    }

    def __init__(self, tonic, scale):
        """Set up the scale, fixing bad args."""

        self.tonic = tonic%12  # Init with lowest octave

        if type(scale) is list or type(scale) is Set:  # Custom scale
            self.members = proof_scale(scale)
        elif type(scale) is str:  # Then caller is giving a common scale name
            if not KNOWN_SCALES.has_key(scale):
                raise ValueError("scale name must be one of the following: "
                    + ", ".join(KNOWN_SCALES.keys()))
            self.members = KNOWN_SCALES.get(scale)
        else:  # bad argument
            raise ValueError(
                "scale must be a list, Set, or recognized scale name.")

    def random_pitch(self, mini, maxi, style, center=-1, spread = -1):
        """Gets a random pitch in this scale.

        Args:
            mini (int): The minimum pitch to return
            maxi (int): The maximum pitch to return
            style (str): The type of random generation. Known types:
                - rand: Uniform distribution
                - tri: Triangular distribution
            center (int): A center value for distributions that need one
            spread (int): A spread value for distributions "" "" ""

        Returns: The random pitch, as a midi note number
        """
        pitch_choices = self.get_choices(mini, maxi, center)

        if (style is "rand"):
            octave = random.randint(mini_oct, maxi_oct)
            pitch = -1
            while pitch>maxi or pitch<mini:
                pitch = octave*12 + self.random_pitch_class()
            return pitch
        elif (style is "tri"):
            pass
        else:
            raise ValueError("Unrecognized random selection type.")

    def pitch_choices(self, mini, maxi, center):
        """Gets the list of pitches to randomly choose from.

        Gets the list of scale pitches that fall between mini and maxi

        Args:
            mini (int): The minimum value to include
            maxi (int): The maximum value to include
            center (int): A value whose index must be kept track of

        Returns:
            A tuple. [0] is the list, [1] is the first tonic's index,
            and [2] is center's index.
        """



    def random_pitch_class(self):
        if type(self.members) is list:
            return random.choice(self.members)
        else:
            return random.choice(tuple(self.members))

    def __len__(self):
        return len(self.members)

def proof_scale(coll):
    """Fixes bad values and duplicates in given pitch class set."""

    coll = Set(coll)
    rm = Set([])
    add = Set([])

    for i in coll:
        if i > 11:
            rm.add(i)
            add.add(i%12)
    # Remove too-big values and replace them with fixed versions
    for bad in rm:
        coll.remove(bad)
    for good in add:
        coll.add(good)

    return coll
