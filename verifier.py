from scipy.io import wavfile
from tqdm import tqdm

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from wave_crypto import WaveCrypto

class WaveVerifier(WaveCrypto):
    def __init__(self, public_key):
        super().__init__(public_key)
        self.verifier = DSS.new(self.key, 'fips-186-3')

    def _attempt_to_verify(self, data, start_index):
        for chunk_start in range(start_index, len(data) - self.chunk_length, self.chunk_length):
            chunk_data = data[chunk_start:chunk_start + self.chunk_length] & ~1

            chunk_hash = SHA256.new(chunk_data.tobytes())
            lsb = self.read_message_from_lsb(data, chunk_start)
            padding = bytes(lsb[self.signature_length // 8:])
            if padding != self.padding:
                return False
            signature = bytes(lsb[:self.signature_length // 8])
            try:
                self.verifier.verify(chunk_hash, signature)
            except ValueError:
                # print(f"Hash does not match signature in sample range {chunk_start} to {chunk_start + self.chunk_length}")
                return False
        return True

    def verify(self, wav_file):
        accurate = True

        # wav_file file: a string filename for a .wav file, currently just 16 bit mono
        # Message: a bytes object
        # TODO: accept other bitrates/multiple channels.
        sample_rate, data = wavfile.read(wav_file)

        # data &= ~1 # Mask off least significant bit of data
        for start_index in tqdm(range(self.chunk_length)):
            if self._attempt_to_verify(data, start_index):
                return True

        return False