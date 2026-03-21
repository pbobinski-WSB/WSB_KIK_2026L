from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

# --- SERWER (BLACK BOX) ---
KEY = os.urandom(32)
NONCE = os.urandom(8)

def get_encrypted_transaction():
    msg = b'<transfer><to>Alice</to><amount>100</amount></transfer>'
    # AES-CTR działa jak szyfr strumieniowy
    ctr = Counter.new(64, prefix=NONCE)
    cipher = AES.new(KEY, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(msg)

def process_transaction(ciphertext):
    ctr = Counter.new(64, prefix=NONCE)
    cipher = AES.new(KEY, AES.MODE_CTR, counter=ctr)
    plaintext = cipher.decrypt(ciphertext)
    print(f"Serwer przetwarza: {plaintext}")
    if b'900' in plaintext:
        print("[!!!] ALARM: Wykryto manipulację kwotą na 900!")
        return True
    return False

c = get_encrypted_transaction()
print(f"Oryginalny szyfrogram (hex): {c.hex()}")
process_transaction(bytes(c))

# Wiemy, że "1" jest na pozycji 32 (policz znaki).
# W kodzie ASCII: '1' to 0x31, '9' to 0x39.
# Różnica (XOR): 0x31 ^ 0x39 = 0x08.
# Zmodyfikuj odpowiedni bajt w 'c', aby po odszyfrowaniu dał '9'.

# modified_c = ...
# process_transaction(modified_c)
# Analiza pozycji:
# <transfer><to>Alice</to><amount>1
# Pozycja znaku '1' to indeks 32.

# Konwertujemy na mutowalną listę bajtów
c_mutable = bytearray(c)

# XORujemy bajt na pozycji 32 z ( '1' ^ '9' )
# '1' ^ X = '9'  =>  X = '1' ^ '9'
xor_diff = ord('1') ^ ord('9') 

c_mutable[32] = c_mutable[32] ^ xor_diff

# Sprawdzamy
process_transaction(bytes(c_mutable))