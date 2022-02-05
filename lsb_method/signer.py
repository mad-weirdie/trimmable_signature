from scipy.io import wavfile
from tqdm import tqdm

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from wave_crypto import WaveCrypto

class WaveSigner(WaveCrypto):
    def __init__(self, private_key):
        super().__init__(private_key)
        self.signer = DSS.new(self.key, 'fips-186-3')

    def sign(self, wav_file, destination_file):



        # wav_file file: a string filename for a .wav file, currently just 16 bit mono
        # Message: a bytes object
        # TODO: accept other bitrates/multiple channels.
        sample_rate, data = wavfile.read(wav_file)

        data &= ~1 # Mask off least significant bit of data

        for chunk_start in tqdm(range(0, len(data) - self.chunk_length, self.chunk_length)):
            chunk_data = data[chunk_start:chunk_start + self.chunk_length]


            chunk_hash = SHA256.new(chunk_data.tobytes())
            signature = self.signer.sign(chunk_hash)

            self.write_message_in_lsb(data, signature + self.padding, chunk_start)

        wavfile.write(destination_file, sample_rate, data)