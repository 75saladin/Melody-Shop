import random

class ScaleIter(object):
    """A class to represent an iterator for a scale.
    
    Attributes:
        scale (Scale): The scale for this iterator
        pitches (list): A list of pitches to choose from
        tonic_low (int): Index of the lowest tonic
        tonic_mid (int): Index of the middlemost tonic
        spacing (int): Distance from tonic to tonic
        prev (int): The previous returned index
    """
    
    def __init__(self, scale, mini, maxi):
        """Sets pitches to [x | mini<=x<=maxi and x is in the scale]"""
        self.scale = scale
        self.pitches = []
        self.spacing = len(scale)
        self.prev = -1
        
        lowest_tonic = 0
        while lowest_tonic < mini:
            lowest_tonic += 12
        
        highest_tonic = lowest_tonic
        while highest_tonic < maxi-12:
            highest_tonic += 12
            
        
        self.pitches.extend(self.partial_octave(lowest_tonic-12, mini, maxi))
        self.tonic_low = len(self.pitches) # next index will be first tonic
        mid_range = (highest_tonic+lowest_tonic)/2
        for p in range(lowest_tonic, highest_tonic, 12):
            self.pitches.extend(self.full_octave(p))
            if p<=mid_range:
                self.tonic_mid = len(self.pitches)
        self.pitches.extend(self.partial_octave(highest_tonic, mini, maxi))
        
    def nextRand(self, style):
        if style is "rand":
            i = random.choice(range(len(self.pitches)))
        elif style is "tri":
            i = int(random.triangular(0, len(self.pitches)-1, self.tonic_mid))
        else:
            raise ValueError("Unrecognized random style")
        
        self.prev = i
        return self.pitches[i]
    
    def nextLine(self, style):
        if style is "tri":
            i = int(random.triangular(0, len(self.pitches)-1, self.prev))
        else:
            raise ValueError("Unrecognized random style")
        
        self.prev = i
        return self.pitches[i]
    
    def partial_octave(self, start, mini, maxi):
        """Returns the notes, in order, from the octave beginning at 
        start that are within mini and maxi.
        
        Args:
            start (int): The pitch to start on. Must be a tonic
            mini (int): The minimum value to include
            maxi (int): The maximum value to include
            
        Returns:
            A list of pitches in the scale
        """
        octave = []
        for p in self.scale.members:
            pitch = start + p
            if pitch>=mini and pitch<=maxi:
                octave.append(start + p)
        return octave
    
    def full_octave(self, start):
        """Returns the notes, in order, from the octave beginning at 
        start.
        
        Args:
            start (int): The pitch to start on. Must be a tonic
            
        Returns:
            A list of pitches in the scale
        """
        octave = []
        for p in self.scale.members:
            octave.append(start + p)
        return octave
            
