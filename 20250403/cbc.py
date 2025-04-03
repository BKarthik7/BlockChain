block_size = 8

def xor(cipher, plain, index, now):
    ans = ""
    i = 0
    while i < now and i < len(plain):
        ans += chr(ord(cipher[i]) ^ ord(plain[index + i]))
        i += 1
    return ans

plain_text = "hello how are you"
initial_vector = "initialy"

def encrypt_cbc(plain_text, initial_vector, block_size):
    cipher_text = ""
    prevcb = initial_vector
    for i in range(0, len(plain_text), block_size):
        block = plain_text[i:i + block_size]
        if len(block) < block_size:
            block = block.ljust(block_size)
        cipher_block = xor(prevcb, block, 0, block_size)
        cipher_text += cipher_block
        prevcb = cipher_block
    return cipher_text

def decrypt_cbc(cipher_text, initial_vector, block_size):
    plain_text = ""
    prevcb = initial_vector
    for i in range(0, len(cipher_text), block_size):
        cipher_block = cipher_text[i:i + block_size]
        plain_block = xor(prevcb, cipher_block, 0, block_size)
        plain_text += plain_block
        prevcb = cipher_block
    return plain_text.strip()

cipher_text = encrypt_cbc(plain_text, initial_vector, block_size)
print("Encrypted:", cipher_text)

decrypted_text = decrypt_cbc(cipher_text, initial_vector, block_size)
print("Decrypted:", decrypted_text)
