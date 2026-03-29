import hashlib

# --- 1. DANE Z NAGŁÓWKA BLOKU (To ma lekki portfel) ---
# Wzięliśmy ten root z wyniku działania Twojego poprzedniego kodu
known_merkle_root = "7d96e0aa23f835a216d66c4d01d3f9ddfa85963e1e5f9d626327980bfa55b09e" 

# --- 2. NASZA TRANSAKCJA (To chcemy zweryfikować) ---
my_tx = "Charlie -> Dave: 0.5 BTC"
my_tx_hash = hashlib.sha256(my_tx.encode()).hexdigest()
my_index = 1 # Charlie był drugi na liście (indeks 1)

# --- 3. DOWÓD OTRZYMANY OD PEŁNEGO WĘZŁA (Merkle Proof) ---
# Skąd się to wzięło? (Z perspektywy pełnego węzła):
# - Drzewo miało 3 transakcje: [Alice, Charlie, Eve]. Zduplikowano Eve -> [Alice, Charlie, Eve, Eve]
# - Żeby z hasha Charliego (indeks 1) dojść do korzenia, Charlie potrzebuje:
#   1. Hasha Alice (bo Alice jest 'siostrą' Charliego na poziomie 0)
#   2. Hasha(Eve + Eve) (bo to jest 'siostra' rodzica Charliego na poziomie 1)

proof_from_node = [
    hashlib.sha256("Alice -> Bob: 1 BTC".encode()).hexdigest(),  # Hash siostry (Alice)
    hashlib.sha256((hashlib.sha256("Eve -> Frank: 0.8 BTC".encode()).hexdigest() * 2).encode()).hexdigest() # Hash ciotki (Eve+Eve)
]

# =====================================================================
# KOD LEKKIEGO PORTFELA (WERYFIKACJA DOWODU SPV)
# Zauważ: Portfel nigdzie nie używa tekstów transakcji Alice czy Eve!
# =====================================================================

def verify_merkle_proof(target_hash, proof_hashes, root, index):
    print(f"[*] Rozpoczynam weryfikację SPV dla transakcji...")
    print(f"    Mój hash: {target_hash}")
    
    current_hash = target_hash
    
    for i, sibling_hash in enumerate(proof_hashes):
        # Sprawdzamy, czy jesteśmy lewym czy prawym węzłem na danym poziomie
        if index % 2 == 0:
            # Jesteśmy po LEWEJ stronie. Siostra jest po PRAWEJ.
            print(f"    Poziom {i}: Hashuję (MójHash + Siostra)")
            combined = current_hash + sibling_hash
        else:
            # Jesteśmy po PRAWEJ stronie. Siostra jest po LEWEJ.
            print(f"    Poziom {i}: Hashuję (Siostra + MójHash)")
            combined = sibling_hash + current_hash
            
        current_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        # Idziemy piętro wyżej w drzewie (dzielenie całkowite przez 2)
        index = index // 2 

    print(f"\n[*] Obliczony Korzeń: {current_hash}")
    print(f"[*] Oczekiwany Korzeń: {root}")
    
    return current_hash == root

# Uruchamiamy weryfikację
is_valid = verify_merkle_proof(my_tx_hash, proof_from_node, known_merkle_root, my_index)

if is_valid:
    print("\n✅ Dowód SPV poprawny! Transakcja JEST w bloku. Nie muszę pobierać reszty bloku!")
else:
    print("\n❌ Oszustwo! Dowód jest fałszywy.")