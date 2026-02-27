from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

KEY = os.urandom(16)

def oracle_encrypt(email):
    # Formatuje string i szyfruje
    prefix = b"email="
    suffix = b"&uid=10&role=user"
    msg = prefix + email.encode() + suffix
    
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(msg, 16))

def oracle_decrypt(ciphertext):
    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        pt = unpad(cipher.decrypt(ciphertext), 16)
        print(f"Odszyfrowano: {pt}")
        if b'role=admin' in pt:
            print("[!!!] ZALOGOWANO JAKO ADMIN!")
    except:
        print("Błąd paddingu")

# Twoje zadanie:
# 1. Wygeneruj szyfrogram, w którym 'admin' (z odpowiednim paddingiem)
#    będzie w osobnym bloku.
# 2. Wygeneruj szyfrogram, w którym końcówka 'role=' będzie na końcu bloku.
# 3. Sklej te kawałki.