import struct


class RC5Service:
    def __init__(self, w=64, r=8, b=32):
        self.w = w
        self.r = r
        self.b = b
        self.t = 2 * (r + 1)
        self.w_bytes = w // 8
        self.mask = (1 << w) - 1

        self.P = 0xB7E151628AED2A6B
        self.Q = 0x9E3779B97F4A7C15

    def _rotate_left(self, val, n):
        n %= self.w
        return ((val << n) & self.mask) | (val >> (self.w - n))

    def _rotate_right(self, val, n):
        n %= self.w
        return (val >> n) | ((val << (self.w - n)) & self.mask)

    def _expand_key(self, password_phrase, md5_service):
        hp_hex = md5_service.hash_text(password_phrase)
        hp = bytes.fromhex(hp_hex)
        hhp = bytes.fromhex(md5_service.hash_text(hp_hex))
        key = hhp + hp

        c = self.b // self.w_bytes
        l_arr = list(struct.unpack('<4Q', key))

        s_table = [0] * self.t
        s_table[0] = self.P
        for i in range(1, self.t):
            s_table[i] = (s_table[i - 1] + self.Q) & self.mask

        i = j = a = b = 0
        for _ in range(3 * max(c, self.t)):
            a = s_table[i] = self._rotate_left((s_table[i] + a + b) & self.mask, 3)
            b = l_arr[j] = self._rotate_left((l_arr[j] + a + b) & self.mask, (a + b))
            i = (i + 1) % self.t
            j = (j + 1) % c
        return s_table

    def _encrypt_block(self, data, s_table):
        a, b = struct.unpack('<2Q', data)
        a = (a + s_table[0]) & self.mask
        b = (b + s_table[1]) & self.mask
        for i in range(1, self.r + 1):
            a = (self._rotate_left(a ^ b, b) + s_table[2 * i]) & self.mask
            b = (self._rotate_left(b ^ a, a) + s_table[2 * i + 1]) & self.mask
        return struct.pack('<2Q', a, b)

    def _decrypt_block(self, data, s_table):
        a, b = struct.unpack('<2Q', data)
        for i in range(self.r, 0, -1):
            b = self._rotate_right((b - s_table[2 * i + 1]) & self.mask, a) ^ a
            a = self._rotate_right((a - s_table[2 * i]) & self.mask, b) ^ b
        a = (a - s_table[0]) & self.mask
        b = (b - s_table[1]) & self.mask
        return struct.pack('<2Q', a, b)

    def encrypt_file(self, in_p, out_p, pw, md5_s, lcg_s):
        s_table = self._expand_key(pw, md5_s)
        nums = lcg_s.generate(4)
        iv = struct.pack('<4I', *[x & 0xFFFFFFFF for x in nums])

        with open(in_p, 'rb') as f_in, open(out_p, 'wb') as f_out:
            f_out.write(self._encrypt_block(iv, s_table))
            prev = iv
            while True:
                chunk = f_in.read(16)
                if not chunk:
                    break
                padding = False
                if len(chunk) < 16:
                    p_len = 16 - len(chunk)
                    chunk += bytes([p_len] * p_len)
                    padding = True

                xor_data = bytes(x ^ y for x, y in zip(chunk, prev))
                encrypted = self._encrypt_block(xor_data, s_table)
                f_out.write(encrypted)
                prev = encrypted
                if padding:
                    break

            if len(chunk) == 16 and not padding:
                chunk = bytes([16] * 16)
                xor_data = bytes(x ^ y for x, y in zip(chunk, prev))
                f_out.write(self._encrypt_block(xor_data, s_table))

    def decrypt_file(self, in_p, out_p, pw, md5_s):
        s_table = self._expand_key(pw, md5_s)
        with open(in_p, 'rb') as f_in:
            iv_enc = f_in.read(16)
            iv = self._decrypt_block(iv_enc, s_table)
            data = f_in.read()

        res, prev = b"", iv
        for i in range(0, len(data), 16):
            curr = data[i:i + 16]
            dec = self._decrypt_block(curr, s_table)
            res += bytes(x ^ y for x, y in zip(dec, prev))
            prev = curr

        pad_len = res[-1]
        with open(out_p, 'wb') as f_out:
            f_out.write(res[:-pad_len])
