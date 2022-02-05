"""
Used for storing a message where we can retrieve it on loop, if we decide to do that. Currently unused.
"""
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