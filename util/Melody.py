class Melody(object):
    """A class to represent a melody.
    
    Attributes:
        pitches (PitchSequence)
        rhythm (RhythmSequence)
        meter (Meter)
    
    ToDo:
        Add other types of sequences:
            Dynamic (amplitude multiplier)
            articulation (amplitude envelope)
            glissando (pitch envelope)
            Vibrato (waviness envelope and frequency envelope)
    """
    
    def __init__(self, pitches, rhythm, meter):
        if len(pitches) is not len(rhythm):
            raise ValueError(
                "A Melody must have the same number of pitches as rhythms.")
        self.pitches = pitches
        self.rhythm = rhythm
        self.meter = meter
        
    def __len__(self):
        return len(self.pitches)
