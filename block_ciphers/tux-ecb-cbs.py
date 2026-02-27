from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def encrypt_image_demo(input_filename):
    # 1. Wczytujemy plik binarnie
    with open(input_filename, 'rb') as f:
        data = f.read()

    # BMP ma zazwyczaj 54 bajty nagłówka.
    # Musimy go zostawić w spokoju, żeby system operacyjny
    # wiedział, że to nadal jest obrazek (rozdzielczość, głębia koloru itd.).
    bmp_header = data[:54] 
    pixel_data = data[54:]

    key = os.urandom(16) # Klucz AES-128
    iv = os.urandom(16)  # IV dla trybu CBC

    # --- TRYB ECB (ZŁY) ---
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    # Musimy dopełnić dane (pad), bo AES wymaga bloków 16-bajtowych
    encrypted_pixels_ecb = cipher_ecb.encrypt(pad(pixel_data, 16))
    
    # Zapisujemy wynik ECB
    with open('tux_encrypted_ECB.bmp', 'wb') as f:
        # Sklejamy oryginalny nagłówek + zaszyfrowane piksele
        # (Ucinamy ewentualny nadmiarowy padding na końcu, żeby plik miał sensowny rozmiar,
        # choć przeglądarki i tak to zignorują)
        f.write(bmp_header + encrypted_pixels_ecb)

    print(f"[OK] Wygenerowano 'tux_encrypted_ECB.bmp'. Otwórz go i zobacz Pingwina!")

    # --- TRYB CBC (DOBRY) ---
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
    encrypted_pixels_cbc = cipher_cbc.encrypt(pad(pixel_data, 16))

    # Zapisujemy wynik CBC
    with open('tux_encrypted_CBC.bmp', 'wb') as f:
        f.write(bmp_header + encrypted_pixels_cbc)

    print(f"[OK] Wygenerowano 'tux_encrypted_CBC.bmp'. To powinien być tylko szum.")

# URUCHOMIENIE
# Upewnij się, że masz plik 'tux.bmp' w tym samym katalogu!
try:
    encrypt_image_demo('tux.bmp')
except FileNotFoundError:
    print("BŁĄD: Nie znaleziono pliku 'tux.bmp'. Pobierz go najpierw.")