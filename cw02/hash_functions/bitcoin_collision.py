import hashlib
import binascii

def sha1(data):
    """Pomocnicza funkcja liczaca SHA-1 (bytes -> bytes)"""
    return hashlib.sha1(data).digest()

def verify_sha1_collision_hex(hex_a, hex_b):
    print("="*60)
    print("DEMO: WERYFIKACJA KOLIZJI SHA-1 (BITCOIN SCRIPT SIM)")
    print("="*60)

    try:
        # Konwersja HEX -> BYTES
        data_a = binascii.unhexlify(hex_a)
        data_b = binascii.unhexlify(hex_b)
    except binascii.Error:
        print("[ERROR] Błąd parsowania HEX stringa! Sprawdź format.")
        return

    print(f"[*] Dane A (bytes): {len(data_a)} bajtów")
    print(f"[*] Dane B (bytes): {len(data_b)} bajtów")

    # KROK 1: Czy dane są RÓŻNE? (OP_EQUAL OP_NOT)
    print("\n[1] Sprawdzanie czy dane wejściowe są różne...")
    if data_a == data_b:
        print("[FAIL] BŁĄD: Ciągi bajtów są identyczne! To nie jest kolizja.")
        return False
    else:
        print("[OK] Dane są RÓŻNE. Warunek OP_NOT spełniony.")

    # KROK 2: Liczenie Hashy (OP_SHA1)
    print("\n[2] Obliczanie skrótów SHA-1...")
    hash_a = sha1(data_a)
    hash_b = sha1(data_b)
    
    # Wyświetlamy hex digest
    digest_a = hash_a.hex()
    digest_b = hash_b.hex()

    print(f"    Hash(A): {digest_a}")
    print(f"    Hash(B): {digest_b}")

    # KROK 3: Czy hashe są IDENTYCZNE? (OP_EQUAL)
    print("\n[3] Porównywanie skrótów...")
    if digest_a == digest_b:
        print("\n" + "*"*50)
        print(" [SUKCES] GRATULACJE! KOLIZJA SHA-1 POTWIERDZONA!")
        print(" Skrypt Bitcoinowy wypłaciłby nagrodę.")
        print("*"*50)
        return True
    else:
        print("\n[FAIL] BŁĄD: Hashe są RÓŻNE.")
        return False

# --- INSTRUKCJA UŻYCIA ---
# Wklej tutaj swoje ciągi HEX z kolizji SHAttered
# (Są bardzo długie, zazwyczaj >300 bajtów każdy)

if __name__ == "__main__":
    # Przykładowe dane (ATRAPY - Zmień na prawdziwe z SHAttered!)
    # Prawdziwe ciągi z ataku SHAttered znajdziesz w plikach PDF
    # (lub mogę Ci podać link do surowych danych, jeśli ich nie masz pod ręką).
    
    # Przykładowe (błędne) dane dla testu skryptu:
    sample_hex_a = "deadbeef" 
    sample_hex_b = "c0ffee"   

    # Dane prawdziwe od Google:
    c1 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db1690901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a21566461309789606bd0bf3f98cda8044629a1'
    c2 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a90901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd309791d06bd0af3f98cda4bc4629b1'


    # Test na atrapach:
    print("--- Test na atrapach (oczekiwany błąd) ---")
    verify_sha1_collision_hex(sample_hex_a, sample_hex_b)

    # Test:
    print("--- Test prawdziwy ---")
    verify_sha1_collision_hex(c1, c2)