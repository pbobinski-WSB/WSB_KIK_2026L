import os

def str_to_bytes(s):
    return s.encode('utf-8')

def xor_bytes(b1, b2):
    # XORuje dwa ciągi bajtów (obcina do długości krótszego)
    return bytes([x ^ y for x, y in zip(b1, b2)])

# 1. Mamy jeden, losowy klucz (OTP)
KEY = os.urandom(32) # 32 bajty losowości

# 2. Dwie wiadomości
msg1 = str_to_bytes("Atakujemy o swicie!")
msg2 = str_to_bytes("Wycofujemy sie juz.")

# 3. Szyfrujemy obie TYM SAMYM kluczem (BŁĄD!)
cipher1 = xor_bytes(msg1, KEY)
cipher2 = xor_bytes(msg2, KEY)

print(f"C1: {cipher1.hex()}")
print(f"C2: {cipher2.hex()}")

# 4. Atakujący przechwytuje C1 i C2. Nie zna klucza.
# Ale robi XOR szyfrogramów:
# (M1 ^ K) ^ (M2 ^ K) = M1 ^ M2 ^ K ^ K = M1 ^ M2 (Klucz znika!)

combined_xor = xor_bytes(cipher1, cipher2)

print(f"\nWynik XOR szyfrogramów (M1 ^ M2):\n{combined_xor.hex()}")

# 5. Co to daje? Jeśli zgadniemy fragment jednej wiadomości (np. wiemy, że to raport wojskowy)
# to odsłonimy fragment drugiej.
# Zgadujemy słowo "Atak":
guess = str_to_bytes("Atak")
revealed = xor_bytes(combined_xor, guess)

print(f"\nZgadując '{guess.decode()}' w M1, w M2 ujawnia się fragment:")
print(f"-> '{revealed}'") 
# Widać fragment "Wyco" - początek drugiej wiadomości!