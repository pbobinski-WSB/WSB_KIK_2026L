import random
import time
import hashlib

# --- SYMULACJA SERWERA (Tego kodu student "nie widzi", ma tylko wynik) ---
# Administrator ustawił seed na moment uruchomienia skryptu (np. przeszłość)
# Symulujemy czas: załóżmy, że skrypt uruchomiono dokładnie w:
# Unix timestamp: 1700000000 (przykładowa data z przeszłości)
secret_seed_time = 1700000000 
random.seed(secret_seed_time)

# Serwer wygenerował tajny klucz (liczbę)
secret_key = random.getrandbits(256)

print(f"Przechwycony klucz (hex): {hex(secret_key)}")
print("Zadanie: Znajdź 'secret_seed_time', wiedząc, że jest to liczba całkowita")
print("z zakresu <1699990000, 1700010000>.")
# ---------------------------------------------------------------------