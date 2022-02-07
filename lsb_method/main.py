"""
Still doesn't handle cropping yet, and only works on 16 bit mono audio.

But now it has classes and inheritance!


also tqdm is just a python library that makes pretty-looking progress bars. If you
don't wanna install it, just change the for loop ranges to normal ranges.
"""
from scipy.io import wavfile

from signer import WaveSigner
from verifier import WaveVerifier

def change_one_sample(filename, lsb_part=False):
    samplerate, data = wavfile.read(filename)
    if lsb_part:
        data[len(data) // 2] += 1
    else:
        data[len(data) // 2] += 2
    wavfile.write(filename, samplerate, data)

def crop_some(filename, crop_start=True, crop_end=True):
    samplerate, data = wavfile.read(filename)
    if crop_start:
        data = data[len(data) // 4:]
    if crop_end:
        data = data[:- (len(data) // 4)]
    wavfile.write(filename, samplerate, data)

if __name__ == '__main__':
    with open('../keys/Alice_private_key.pem','r') as f:
        private_key = f.read()

    with open('../keys/Alice_public_key.pem','r') as f:
        public_key = f.read()

    original_file = '../audio_samples/half_second_tone.wav'
    signed_file = '../tone_s.wav'

    s = WaveSigner(private_key)
    print('signing')
    s.sign(original_file, signed_file)
    v = WaveVerifier(public_key)
    # Uncomment this next line to see what happens when the verification fails!
    # change_one_sample(signed_file, lsb_part=True)
    # trim the start and end of the file
    crop_some(signed_file)
    print('verifying')
    result = v.verify(signed_file)
    if result:
        print("Verified correctly. The real deal!")
    else:
        print("Not verified correctly. The song has been tampered with.")
