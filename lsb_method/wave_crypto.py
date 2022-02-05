from Crypto.PublicKey import ECC

class WaveCrypto:
    def __init__(self, key):
        self.key = ECC.import_key(key)

        self.padding = bytearray([0, 0, 0, 0])

        self.signature_length = 64 * 8  # bits
        # Since the algorithm for signing is P-256, the signatures are 64 bytes
        # long, or 64 * 8 bits long.
        # See https://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html

        self.padding_length = len(self.padding) * 8  # bits

        self.chunk_length = self.signature_length + self.padding_length

    def get_bit_of_byte(self, byte, bit_index):
        # 0 index is least significant
        return byte >> bit_index & 1

    def write_message_in_lsb(self, array, message, start_index):
        # print(len(message) * 8, self.chunk_length)
        assert len(message) * 8 == self.chunk_length
        for i in range(self.chunk_length):
            bit = self.get_bit_of_byte(message[(i) // 8], i % 8)
            array[i + start_index] += bit

    def bit_array_to_bytes(self, bit_array):
        arr = bytearray([0 for i in range(len(bit_array) // 8)])
        for i in range(len(bit_array)):
            arr[i // 8] += bit_array[i] << (i % 8)
        return arr

    def read_message_from_lsb(self, array, start_index):
        bits = []
        for i in range(self.chunk_length):
            bits.append(array[start_index + i] & 1)

        return self.bit_array_to_bytes(bits)