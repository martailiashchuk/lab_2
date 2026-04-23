import struct
import math
import os


class MD5Service:
    def __init__(self):
        self.T = [int(4294967296 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
        self.S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + \
                 [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    def _rotate_left(self, x, n):
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def _process_block(self, chunk, h0, h1, h2, h3):
        X = list(struct.unpack('<16I', chunk))
        A, B, C, D = h0, h1, h2, h3
        for j in range(64):
            if j < 16:
                f, g = (B & C) | (~B & D), j
            elif j < 32:
                f, g = (D & B) | (~D & C), (5 * j + 1) % 16
            elif j < 48:
                f, g = B ^ C ^ D, (3 * j + 5) % 16
            else:
                f, g = C ^ (B | ~D), (7 * j) % 16

            temp = (A + f + self.T[j] + X[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + self._rotate_left(temp, self.S[j])) & 0xFFFFFFFF

        return (h0 + A) & 0xFFFFFFFF, (h1 + B) & 0xFFFFFFFF, (h2 + C) & 0xFFFFFFFF, (h3 + D) & 0xFFFFFFFF

    def hash_text(self, message):
        data = bytearray(message, 'utf-8')
        orig_len_bits = (len(data) * 8) & 0xFFFFFFFFFFFFFFFF
        data.append(0x80)
        while len(data) % 64 != 56: data.append(0)
        data += struct.pack('<Q', orig_len_bits)

        h0, h1, h2, h3 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
        for i in range(0, len(data), 64):
            h0, h1, h2, h3 = self._process_block(data[i:i + 64], h0, h1, h2, h3)
        return self._format_hash(h0, h1, h2, h3)

    def hash_file(self, filepath):
        h0, h1, h2, h3 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
        file_size = os.path.getsize(filepath)
        orig_len_bits = (file_size * 8) & 0xFFFFFFFFFFFFFFFF

        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk or len(chunk) < 4096:
                    return self._finalize_file(chunk, orig_len_bits, h0, h1, h2, h3)

                for i in range(0, len(chunk), 64):
                    h0, h1, h2, h3 = self._process_block(chunk[i:i + 64], h0, h1, h2, h3)

    def _finalize_file(self, last_chunk, total_bits, h0, h1, h2, h3):
        data = bytearray(last_chunk if last_chunk else b"")
        data.append(0x80)
        while len(data) % 64 != 56: data.append(0)
        data += struct.pack('<Q', total_bits)

        for i in range(0, len(data), 64):
            h0, h1, h2, h3 = self._process_block(data[i:i + 64], h0, h1, h2, h3)
        return self._format_hash(h0, h1, h2, h3)

    def _format_hash(self, h0, h1, h2, h3):
        return ''.join(format(x, '02x') for x in struct.unpack('16B', struct.pack('<4I', h0, h1, h2, h3))).upper()