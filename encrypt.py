"""
Just getting started... Doesn't handle cropping yet, and only works on 16 bit mono audio.
From what I'm reading I think the way I'm doing the encryption is kind of a faux pas:
I thought that digitally signing was just encrypting with the rsa private key, turns out i'm wrong:
https://crypto.stackexchange.com/questions/15997/is-rsa-encryption-with-a-private-key-the-same-as-signature-generation

Currently this code makes the private key public and vice-versa, which probably leaves
Rivest, Shamir, and Adleman immediately dying, just so they can roll around in their
graves.

So I guess the next thing I'll do is change that to do digital signature the right way,
but I wanted to show ya'll some quick and dirty code.

also tqdm is just a python library that makes pretty-looking progress bars. If you
don't wanna install it, just change the for loop ranges to normal ranges.
"""

import rsa
from scipy.io import wavfile
import numpy as np
from tqdm import tqdm

padding = bytearray([0,0,0,0])
chunk_hash_size = 28 # bytes, since we're using SHA-224 bits

class MessageBuffer:
    def __init__(self, message):
        self.message = message
        self.index = 0

    def get_next(self, n=1):
        arr = bytearray(b'')
        for i in range(n):
            arr.append(self.message[self.index])
            self.index += 1
            self.index %= len(self.message)
        return arr

def get_bit_of_byte(byte, bit_index):
    # 0 index is least significant
    return byte >> bit_index & 1

def bit_array_to_bytes(bit_array):
    arr = bytearray([0 for i in range(len(bit_array) // 8)])
    for i in range(len(bit_array)):
        arr[i // 8] += bit_array[i] << (i % 8)
    return arr


def encrypt(filename, outfile_name, message, key):

    chunk_size = 512 + len(padding) * 8
    # print("chunk size:", chunk_size)

    message = message.encode('ascii')
    message += b'\0'
    sample_rate, data = wavfile.read(filename)
    data = data & ~1  # Mask off least significant bit


    message_buffer = MessageBuffer(message)
    for start_of_chunk in tqdm(range(0,len(data) - chunk_size, chunk_size)):
        chunk_data = data[start_of_chunk:start_of_chunk + chunk_size]
        chunk_hash = bytearray(rsa.compute_hash(chunk_data.tobytes(), 'SHA-224'))

        max_rsa_message_size = 53
        message_segment = message_buffer.get_next(max_rsa_message_size - chunk_hash_size)
        encrypted_message = bytearray(rsa.encrypt(chunk_hash + message_segment, key))
        encrypted_message += padding
        # print(encrypted_message)
        for i in range(chunk_size):
            bit = get_bit_of_byte(encrypted_message[i // 8], i % 8)
            data[start_of_chunk + i] += bit

    wavfile.write(outfile_name, sample_rate, data)

def decrypt(filename, key):

    chunk_size = 512 + len(padding) * 8
    print("chunk size:", chunk_size)

    sample_rate, data = wavfile.read(filename)

    message = bytearray()
    for start_of_chunk in tqdm(range(0,len(data) - chunk_size, chunk_size)):
        chunk_data = data[start_of_chunk:start_of_chunk + chunk_size]
        significant_part = chunk_data & ~1
        chunk_hash = bytearray(rsa.compute_hash(significant_part.tobytes(), 'SHA-224'))
        lsb_part = bit_array_to_bytes(chunk_data & 1)[:-4]
        decrypted = rsa.decrypt(lsb_part, key)
        # print(decrypted)
        hash_verification = decrypted[:chunk_hash_size]
        if hash_verification != chunk_hash:
            print(hash_verification, chunk_hash)
            print("Hashes don't match, file has been tampered with!")
            return
        message += decrypted[chunk_hash_size:]


    print(message)
    # wavfile.write(outfile_name, sample_rate, data)

if __name__ == '__main__':

    public_key, private_key = rsa.newkeys(512)
    encrypt('audio_samples/monkeys_mono.wav','monkeys_mono_encrypted.wav','Hello darkness my old friend',public_key)
    decrypt('monkeys_mono_encrypted.wav', private_key)