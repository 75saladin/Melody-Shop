class MSequence(object):
    """A class to represent a sequence of musical aspects.

    eg pitch, rhythm, interval, chord, etc.
    
    Attributes:
        sequence (list)
    """
    
    def __init__(self):
        self.sequence = None
        
    def retrograde():
        sequence = sequence[::-1]
    
    def __len__(self):
        """Gets the number of notes in this sequence."""
        return len(self.sequence)
    
    def __str__(self):
        return str(self.sequence)
