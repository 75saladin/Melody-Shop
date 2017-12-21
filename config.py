import random

fuzz = 5
scale = "mjpent"
tempo = 600
tonic = random.randint(1,6)
beat = "hip"
div = "4"
bass_beat = "square"

##############################################################################
mbeats = {
    "hip": [2, 0, 3, 1],
    "square": [0, 2, 1, 3]
}
mdivs = {
    "4": [2, 2, 2]
}
