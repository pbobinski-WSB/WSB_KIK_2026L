def lfsr(seed, mask):
    """Prosty 4-bitowy LFSR."""
    state = seed
    while True:
        # Zwracamy ostatni bit
        output_bit = state & 1
        yield output_bit
        
        # Obliczamy nowy bit (tapping)
        new_bit = 0
        temp_state = state & mask
        # XOR wszystkich bitów wskazanych przez maskę
        while temp_state > 0:
            new_bit ^= (temp_state & 1)
            temp_state >>= 1
            
        # Przesuwamy rejestr i wstawiamy nowy bit na początek
        state = (state >> 1) | (new_bit << 3) # dla 4 bitów

# Przykład użycia
generator = lfsr(0b1001, 0b1100) # seed, maska (wielomian)
print("Strumień bitów LFSR:", [next(generator) for _ in range(10)])