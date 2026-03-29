import hashlib

def get_binary_string(data):
    # Oblicza SHA-256 i zwraca jako ciąg '0101...'
    h = hashlib.sha256(data).digest()
    return ''.join(f'{b:08b}' for b in h)

def hamming_distance(s1, s2):
    # Liczy ile bitów się różni
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# 1. Oryginalna wiadomość
msg1 = b"Kryptografia"
bin1 = get_binary_string(msg1)

# 2. Zmieniamy OSTATNI BIT ostatniego znaku ('a' -> '`')
# 'a' = 01100001, '`' = 01100000
msg2 = b"Kryptografid" # Zmieniłem ostatnią literę minimalnie
bin2 = get_binary_string(msg2)

# 3. Porównanie
diff = hamming_distance(bin1, bin2)
total_bits = 256

print(f"Msg1: {msg1}")
print(f"Msg2: {msg2}")
print(f"Różnica w wejściu: mała zmiana")
print(f"Bin1: {bin1}")
print(f"Bin2: {bin2}")

print(f"Różnica w wyjściu (bity): {diff}/{total_bits}")
print(f"Zmiana procentowa: {diff/total_bits*100:.2f}%")

# Oczekiwany wynik: ok. 50%. Jeśli byłoby np. 1%, hash jest do niczego.