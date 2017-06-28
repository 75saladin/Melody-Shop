from operator import mul

class Meter(object):
    """A musical meter.
    
    A class to represent a heirarchy of importance of each even division
    of some length of time.
    
    Attributes:
        priority (list): A measure in the meter, divided into equal
            sub-beats. Each beat index contains its importance ranking.
        beats (int): The number of beats per bar in this meter
    """
    
    def __init__(self, beat_scheme, division):
        """Builds a list of with rankings of importance of sequential 
        divisions of each beat and sub-beat in the beat scheme.
        
        Args:
            beat_scheme (list): A chronological list of beat importance
                rankings. Must be a permutation of integers from 0 to 
                len(beat_scheme)-1.
            division (list): The divisions of the beat. For each <int> 
                in the list, each beat in the beat scheme will divide 
                each of the current smallest sub-beats into <int> even
                sub-beats.
        
        len(priority) = len(beat_scheme)*product(division)
        """
        
        # Final number of sub-beats will be (#of beats * each division)
        self.beats = len(beat_scheme)
        length = len(beat_scheme)*reduce(mul, division, 1)
        subbeats_per = length/len(beat_scheme)
        self.priority = [None]*length # Gross, but only way to place staggeredly
        
        # spread the beat scheme evenly into the big list
        for i in range(0, len(beat_scheme)):
            self.priority[i*subbeats_per] = beat_scheme[i]
        
        # The length of unfilled segment following a filled sub-beat
        working_length = subbeats_per 
        for h in range(len(division)):  # for each division of the beat
            d = division[h]
            skip = working_length/d
            
            to_examine = []
            # Look for filled values that can branch to fill empties
            for i in range(len(self.priority)):
                if self.priority[i] is not None: to_examine.append(i)
                
            # Do branch on filled places. New fills get ignored
            for i in to_examine:
                sb = self.priority[i]
                for j in range(skip, working_length, skip):
                    self.priority[i+j] = sb+pow(2, h)*len(beat_scheme)
            working_length /= d
            
    def __len__(self):
        return len(self.priority)
        
        
