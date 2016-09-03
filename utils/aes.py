import pyaes


class AES:
    @staticmethod
    def decrypt_ige(cipher_text, key, iv):
        iv1 = iv[:len(iv)//2]
        iv2 = iv[len(iv)//2:]

        aes = pyaes.AES(key)

        plain_text = [0] * len(cipher_text)
        blocks_count = len(cipher_text) // 16

        cipher_text_block = [0] * 16
        for block_index in range(blocks_count):
            for i in range(16):
                cipher_text_block[i] = cipher_text[block_index * 16 + i] ^ iv2[i]

            plain_text_block = aes.decrypt(cipher_text_block)

            for i in range(16):
                plain_text_block[i] ^= iv1[i]

            iv1 = cipher_text[block_index * 16:block_index * 16 + 16]
            iv2 = plain_text_block[0:16]

            plain_text[block_index * 16:block_index * 16 + 16] = plain_text_block[:16]

        return bytes(plain_text)

    @staticmethod
    def encrypt_ige(plain_text, key, iv):
        # TODO: Random padding
        padding = bytes(16 - len(plain_text) % 16)
        plain_text += padding

        iv1 = iv[:len(iv)//2]
        iv2 = iv[len(iv)//2:]

        aes = pyaes.AES(key)

        blocks_count = len(plain_text) // 16
        cipher_text = [0] * len(plain_text)

        for block_index in range(blocks_count):
            plain_text_block = list(plain_text[block_index * 16:block_index * 16 + 16])
            for i in range(16):
                plain_text_block[i] ^= iv1[i]

            cipher_text_block = aes.encrypt(plain_text_block)

            for i in range(16):
                cipher_text_block[i] ^= iv2[i]

            iv1 = cipher_text_block[0:16]
            iv2 = plain_text[block_index * 16:block_index * 16 + 16]

            cipher_text[block_index * 16:block_index * 16 + 16] = cipher_text_block[:16]

        return bytes(cipher_text)
