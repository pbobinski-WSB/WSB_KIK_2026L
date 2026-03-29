import hashlib
import time

# Parametry nagłówka bloku
previous_block_hash = "000000abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234"  # Hash poprzedniego bloku
merkle_root_hash = "7d96e0aa23f835a216d66c4d01d3f9ddfa85963e1e5f9d626327980bfa55b09e"  # Hash drzewa Merkle
target_prefix = "000000"  # Trudność kopania (hash musi zaczynać się od "0000")

# Kopanie bloku (Proof of Work)
def mining (target_prefix = "0000"):
    nonce = 0
    start_time = time.time()
    while True:
        # Tworzymy zawartość bloku (uproszczona)
        block_header = f"{previous_block_hash}{merkle_root_hash}{nonce}"
        
        # Obliczamy hash bloku
        block_hash = hashlib.sha256(block_header.encode()).hexdigest()
        
        # Sprawdzamy, czy hash spełnia warunek trudności
        if block_hash.startswith(target_prefix):
            end_time = time.time()
            print("\n✅ Znaleziono poprawny blok!")
            print(f"Nonce: {nonce}")
            print(f"Hash bloku: {block_hash}")
            print(f"Czas kopania: {end_time - start_time:.2f} sekundy")
            break  # Kopanie zakończone
        
        # Jeśli nie, zwiększamy nonce i próbujemy dalej
        nonce += 1
    return end_time - start_time

t3 = mining("000")
t4 = mining()
t5 = mining("00000")
t6 = mining("000000")
print(f"{t3:.2f} s, {t4:.2f} s, {t5:.2f} s, {t6:.2f} s")