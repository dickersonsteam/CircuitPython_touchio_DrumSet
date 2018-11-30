import touchio
import board
import audioio
import time

# the capacitance threshold in touchio defaults to 100
# use touch_delta to change that default value
touch_delta = 200

# the number of pads and the number of samples should match
pads = [touchio.TouchIn(board.A1),
        touchio.TouchIn(board.A2),
        touchio.TouchIn(board.A3),
        touchio.TouchIn(board.A4)]

# set the new threshold value for each pad    
for pad in pads:
    pad.threshold = pad.raw_value + touch_delta
    
# list all samples here
# there should be the same number of samples and pads
samples = [audioio.WaveFile(open("kick.wav", "rb")),
           audioio.WaveFile(open("snare.wav", "rb")),
           audioio.WaveFile(open("hihat.wav", "rb")),
           audioio.WaveFile(open("crash.wav", "rb"))]

# initialize speaker output pin
# on Feather M0 boards, this must be A0
audio_pin = audioio.AudioOut(board.A0)

# create mixer object with the number of voices required
mixer = audioio.Mixer(voice_count=4,
                      sample_rate=22050,
                      channel_count=1,
                      bits_per_sample=16,
                      samples_signed=True)

# start outputing the mixer to the DAC
audio_pin.play(mixer)

was_released = []
for i in pads:
    was_released.append(True)


# def test_pads():
# Call this function to prompt the user to test each
# of the capacitive touch pads
def test_pads():
    print("Test Pads")
    
    for i, pad in enumerate(pads):
        print("Push Pad " + str(i))
        while not pad.value:
            pass
        print(str(i))
        print("Button " + str(i) + " works.")
    
    print("All buttons work.")


# before main body loop
# test all touch pads
test_pads()

# main body loop
# check buttons and play sample in mixer
while True:
   
    for index, pad in enumerate(pads):
        if pad.value and was_released[index]:
            was_released[index] = False
            mixer.play(samples[index], voice=index)
            print("Playing sample " + str(index) + ".")
        elif pad.raw_value < (pad.threshold - (touch_delta/2)):  # hysteresis
            was_released[index] = True
        
    # debounce delay
    time.sleep(0.01)
    