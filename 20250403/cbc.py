no_of_words = 8
def xor(cipher, plain, index, now):
    ans = ""
    i = 0
    while(i < now and i < len(plain)):
        ans += chr(int(cipher[i]) ^ int(plain[index+i]))
        i += 1
    return ans

plain_text = "hello how are you"
initial_vector = "initial"
print(xor(initial_vector, plain_text, 0, no_of_words))
