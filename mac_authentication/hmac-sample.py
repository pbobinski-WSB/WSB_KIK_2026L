import hmac
import hashlib

key = b'tajny_klucz'
msg = b'Transfer 1000 PLN'

# Nadawca
tag = hmac.new(key, msg, hashlib.sha256).hexdigest()
print(f"Wiadomość: {msg}, Tag: {tag}")

# Atakujący zmienia treść
msg_fake = b'Transfer 9000 PLN'
# Ale nie zna klucza, więc nie wygeneruje poprawnego tagu
tag_fake = hmac.new(key, msg_fake, hashlib.sha256).hexdigest() # To zrobiłby serwer

print(f"Wiadomość FAKE: {msg_fake}, Tag FAKE: {tag_fake}")

if hmac.compare_digest(tag, tag_fake):
    print("Weryfikacja OK")
else:
    print("BŁĄD! Naruszona integralność.")