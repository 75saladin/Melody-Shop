import random
from Scale import *
from ScaleIter import *
from MSequence import *

class PitchSequence(MSequence):
    """A class to represent a sequence of pitches.
    
    Global constants:
        MINI (int): The lowest allowed pitch when unspecified
        MAXI (int): The highest allowed pitch when unspecified
        
    Attributes:
        sequence (inherited): The sequence of pitches, as midi note #s
    """
    
    global MINI
    global MAXI
    MINI = 20
    MAXI = 110
    
    
    def __init__(self):
        MSequence.__init__(self)
    
    def gen_from_scale(self, size, scale, line, style="rand", mini=MINI, maxi=MAXI):
        """Populates the sequence with random pitches from the scale
        
        Args:
            size (int): The number of pitches to generate.
                ie the length of the sequence
            scale (Scale): The scale to get pitches from
            line (bool): Whether or not to generate a line. If true, the
                previous value will be considered to generate the next.
            style (str): The style of random choice. Options:
                - "rand": Only works if line is false. uniform random.
                - "tri": Triangular distribution. If line, center is 
                    previous note. If not, center is middlemost tonic.
            mini (int): The minimum pitch to include.
            maxi (int): The maximum pitch to include
        """
        self.sequence = []
        iterator = ScaleIter(scale, mini, maxi)
        if line:
            for i in range(0, size):
                self.sequence.append(iterator.nextLine(style))
        else:
            for i in range(0, size):
                self.sequence.append(iterator.nextRand(style))
            
