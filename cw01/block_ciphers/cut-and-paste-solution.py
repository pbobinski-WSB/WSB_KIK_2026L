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


szyfr = oracle_encrypt('pbo@pbo.pl')
print(szyfr)
oracle_decrypt(szyfr)

# Rozwiązanie w Pythonie:
# Potrzebujemy bloku z treścią "admin" + padding PKCS7
# Padding dla "admin" (5 znaków) w bloku 16 to 11 znaków o wartości chr(11)
pkcs7_pad = b'admin' + (b'\x0b' * 11) 
# Żeby ten blok pojawił się jako drugi, musimy wypchnąć pierwszy blok (email= ma 6 znaków, brakuje 10)
# email = 'A'*10 + pkcs7_pad
payload_email = (b'A' * 10) + pkcs7_pad
c1 = oracle_encrypt(payload_email.decode())
admin_block = c1[16:32] # Wyciągamy interesujący nas blok

# Teraz musimy spreparować początek, żeby kończył się na "role="
# email= (6) + X + &uid=10&role= (13) = k*16
# 19 + X = 32 => X = 13 znaków
email_len = 13
c2 = oracle_encrypt("A" * email_len)
# Interesują nas pierwsze 32 bajty (2 bloki), resztę (gdzie jest "user") odcinamy
target_prefix = c2[:32]

# Sklejamy
final_attack = target_prefix + admin_block
print(final_attack)
oracle_decrypt(final_attack)