from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# --- CZĘŚĆ 1: SERWER (OFIARA) ---
# Serwer ma klucz, którego NIE ZNAMY.
_SECRET_KEY = os.urandom(16)

def encrypt_data(plaintext):
    """
    To robi serwer: Szyfruje dane i wysyła do klienta (IV + Szyfrogram).
    """
    # Losowe IV dla każdego szyfrowania
    iv = os.urandom(16)
    cipher = AES.new(_SECRET_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), 16))
    return iv, ciphertext

def padding_oracle(iv, ciphertext):
    """
    To jest nasza WYROCZNIA.
    Symuluje odpowiedź serwera na otrzymany request.
    Zwraca True (kod 200/403) jeśli padding jest poprawny.
    Zwraca False (kod 500) jeśli padding jest błędny.
    """
    cipher = AES.new(_SECRET_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    
    try:
        # Próba zdjęcia paddingu. Jeśli padding jest zły (np. kończy się na 0x05, 0x02...),
        # biblioteka rzuci błąd ValueError. To jest nasze "500 Internal Server Error".
        unpad(decrypted, 16)
        return True
    except ValueError:
        return False

# --- CZĘŚĆ 2: ATAKUJĄCY (MY) ---

def run_attack(iv_original, ciphertext):
    print(f"[*] Przechwycono IV: {iv_original.hex()}")
    print(f"[*] Przechwycono CT: {ciphertext.hex()}")
    print("-" * 50)
    
    # Tutaj będziemy składać odzyskany tekst
    decrypted_plaintext = bytearray(16)
    
    # Tablica na "Intermediate State" (Stan Pośredni - to co wychodzi z AES przed XORem z IV)
    intermediate_state = bytearray(16)

    # Pętla po bajtach od ostatniego (15) do pierwszego (0)
    for byte_index in range(15, -1, -1):
        
        # 1. Ustalmy jaki padding chcemy uzyskać.
        # Dla ostatniego bajtu (indeks 15) chcemy padding 0x01 (długość 1)
        # Dla przedostatniego (indeks 14) chcemy padding 0x02 (długość 2) itd.
        target_padding_len = 16 - byte_index
        target_padding_val = target_padding_len
        
        # 2. Budujemy fałszywe IV (fake_iv)
        fake_iv = bytearray(16)
        
        # 3. Ustawiamy końcówkę fake_iv tak, aby ZNANE już bajty po odszyfrowaniu dawały
        # oczekiwany padding (np. 0x02, 0x03 itd.)
        # Matematyka: fake_iv[k] = intermediate[k] ^ target_padding
        for k in range(byte_index + 1, 16):
            fake_iv[k] = intermediate_state[k] ^ target_padding_val

        # 4. Atakujemy aktualny bajt (byte_index) metodą brute-force (0..255)
        found = False
        for guess in range(256):
            # Ustawiamy zgadywany bajt w fake_iv
            fake_iv[byte_index] = guess
            
            # WYSYŁAMY DO WYROCZNI
            # Pytamy: "Czy to fake_iv + ciphertext ma poprawny padding?"
            if padding_oracle(bytes(fake_iv), ciphertext):
                
                # BINGO! Wyrocznia powiedziała TAK.
                # To oznacza, że: Decrypt(C)[byte_index] ^ guess == target_padding_val
                # Więc możemy obliczyć bajt stanu pośredniego:
                discovered_intermediate_byte = guess ^ target_padding_val
                intermediate_state[byte_index] = discovered_intermediate_byte
                
                # A teraz odzyskujemy ORYGINALNY tekst jawny:
                # Plaintext = Intermediate ^ Original_IV
                original_byte = discovered_intermediate_byte ^ iv_original[byte_index]
                decrypted_plaintext[byte_index] = original_byte
                
                print(f"Bajt {byte_index:02d} złamany! Wartość: '{chr(original_byte)}' (hex: {original_byte:02x})")
                found = True
                break
        
        if not found:
            print(f"[!] Nie udało się znaleźć bajtu {byte_index}. Coś poszło nie tak.")
            break

    return bytes(decrypted_plaintext)

# --- URUCHOMIENIE ---

# 1. Sytuacja normalna: Użytkownik loguje się
secret_msg = "TajneHaslo"
real_iv, real_ct = encrypt_data(secret_msg)

# 2. Atak: Haker przechwycił dane i nie zna klucza, ale ma dostęp do padding_oracle()
print("Rozpoczynam atak Padding Oracle...")
recovered = run_attack(real_iv, real_ct)

print("-" * 50)
print(f"SUKCES! Odzyskana wiadomość: {recovered}")
# Usuwamy padding z wyniku, żeby zobaczyć czysty tekst (dla estetyki)
try:
    print(f"Tekst czysty: {unpad(recovered, 16).decode()}")
except:
    print("Błąd unpadingu wyniku końcowego")