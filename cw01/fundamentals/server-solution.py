import random

# Przechwycona wartość (student kopiuje to z wyniku działania skryptu startowego)
# Dla seed = 1700000000, getrandbits(256) w Python 3 daje poniższą wartość:
target_hex = "0xb1c07668d1797b7ff63cbed91e68977d6b4b2d0c310f9fcb579cfc715210160b"
target_key = int(target_hex, 16)

# Zakres poszukiwań (np. +/- 24h od domniemanego czasu)
# W zadaniu daliśmy węższy zakres dla szybkości demo
start_time = 1699990000
end_time   = 1700010000

print("Rozpoczynam łamanie seeda...")

found = False
for t in range(start_time, end_time):
    # 1. Ustawiamy ten sam stan generatora co serwer
    random.seed(t)
    
    # 2. Generujemy to samo co serwer
    generated_key = random.getrandbits(256)
    
    # 3. Sprawdzamy czy pasuje
    if generated_key == target_key:
        print(f"\n[SUKCES] Znaleziono seed! Timestamp: {t}")
        print(f"Sprawdzenie: random.seed({t}) -> {hex(generated_key)}")
        found = True
        break

if not found:
    print("Nie znaleziono seeda w tym zakresie.")