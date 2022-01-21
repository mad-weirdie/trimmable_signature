from scipy.io import wavfile
from tqdm import tqdm

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from wave_crypto import WaveCrypto

class WaveVerifier(WaveCrypto):
    def __init__(self, public_key):
        super().__init__(public_key)

    def verify(self, wav_file):
        accurate = True
        verifier = DSS.new(self.key, 'fips-186-3')
        #TODO: is it bad to reuse the verifier? should we be declaring it at init?

        # wav_file file: a string filename for a .wav file, currently just 16 bit mono
        # Message: a bytes object
        # TODO: accept other bitrates/multiple channels.
        sample_rate, data = wavfile.read(wav_file)

        # data &= ~1 # Mask off least significant bit of data

        for chunk_start in tqdm(range(0, len(data) - self.chunk_length, self.chunk_length)):
            chunk_data = data[chunk_start:chunk_start + self.chunk_length] & ~1

            chunk_hash = SHA256.new(chunk_data.tobytes())
            lsb = self.read_message_from_lsb(data, chunk_start)

            signature = bytes(lsb[:self.signature_length // 8])
            try:
                verifier.verify(chunk_hash, signature)
            except ValueError:
                print(f"Hash does not match signature in sample range {chunk_start} to {chunk_start + self.chunk_length}")
                accurate = False
                break
        return accurate