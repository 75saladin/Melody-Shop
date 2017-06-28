import random
import sys
from MSequence import *

class RhythmSequence(MSequence):
    """A class to represent a sequence of note lengths.
    
    Attributes:
        sequence (inherited): The sequence of note lengths. A note 
            length is the number of sub-beats it fills.
        length (int): The total length of the rhythm. ie, sum of sequence
    """
    
    def __init__(self):
        MSequence.__init__(self)
    
    def gen_random(self, size, notes=None, max=sys.maxint):
        """Generates a random sequence.
        
        Args:
            size (int): The number of sub-beats to fill
            notes (int): The number of notes to use (ie target length)
            max (int): The maximum note value.
        """
        
        if notes is None: 
            notes = random.randint(1, size)
        self.gen_random_frontloaded(size, notes, max)
        random.shuffle(self.sequence)
        
    def gen_random_frontloaded(self, size, notes, max=sys.maxint):
        """Generates a random sequence with larger values toward the front"""
        
        self.sequence = []
        summ = 0
        for i in range(notes):
            if i is notes-1: # This is the last note and must fill
                leng = size-summ
            else:
                leng = random.randint(1, min(size-summ-(notes-i-1), max))
            summ += leng
            self.sequence.append(leng)
        self.length = sum(self.sequence)
        
    def gen_evenly(self, size, notes):
        avg_note_len = size/float(notes)
        self.sequence = []
        
        if size%notes is 0: # This divides evenly into target #of notes
            for i in range(notes):
                self.sequence.append(int(avg_note_len))
            return
        
        
        # Keep track of remaining cells and remaining notes. Maintain rnotes/rcells close to avg_note_len
        rnotes = float(notes)
        rcells = size
        for i in range(notes):
            ravg = rcells/rnotes
    
            if ravg > avg_note_len: # a bit too many cells for the remaining notes
                # so favor the large note value
                next = int(avg_note_len+1)
            elif ravg < avg_note_len: # a bit too few cells for the remaining notes
                # so favor the small note value
                next = int(avg_note_len)
            else:
                # default to favor large note value
                next = int(avg_note_len+1)
            self.sequence.append(int(next))
            rnotes -= 1
            rcells -= next
            
        
    def gen_from_meter(self, meter, notes, iterations, style="even", max=sys.maxint):
        if style is "even":
            self.gen_evenly(len(meter), notes)
        elif style is "rand":
            self.gen_random(len(meter), notes, max)
        elif style is "randf":
            self.gen_random_frontloaded(len(meter), notes, max)
        else: raise TypeError("Unrecognized rhythm generation style")
        
        for i in range(iterations):
            added = 0
            len_so_far = 0
            for j in range(len(self.sequence)-1):
                n = self.sequence[j]
                # Do a fuzz: increase or decrease note length to get next beat
                # to start on a smaller meter value than it did before. If both
                # work, pick the one that gets <added> closer to -1
                next_sb = len_so_far + n
                next_pri = meter.priority[next_sb]
                left_pri = meter.priority[next_sb-1]
                if next_sb+1 < len(meter.priority): 
                    right_pri = meter.priority[next_sb+1]
                else:
                    right_pri = sys.maxint# Don't go off list edge
                len_so_far += n  # Then dec for shrink or inc for grow
                if left_pri < next_pri and right_pri < next_pri:
                    # Both are better, get added closer to -1
                    if added > -1 and n>1:  # Shrink
                        self.sequence[j] = n-1
                        len_so_far -= 1
                        added -= 1
                    elif added < -1:  # Grow
                        self.sequence[j] = n+1
                        len_so_far += 1
                        added += 1
                    else:
                        # Prefer shrink
                        if n>1:
                            self.sequence[j] = n-1
                            len_so_far -= 1
                            added -= 1
                elif left_pri < next_pri and right_pri > next_pri and n>1:
                    # left is better, shrink
                    self.sequence[j] = n-1
                    len_so_far -= 1
                    added -= 1
                elif left_pri > next_pri and right_pri < next_pri:
                    # right is better, grow
                    self.sequence[j] = n+1
                    len_so_far += 1
                    added += 1
                elif left_pri > next_pri and right_pri > next_pri:
                    #neither is better, do nothing
                    pass
                
        self.sequence[len(self.sequence)-1] = len(meter)-len_so_far
