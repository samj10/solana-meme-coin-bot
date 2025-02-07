
from solders.keypair import Keypair
keypair = Keypair()
valid_base58_key = str(keypair)  # Directly returns Base58 string:cite[5]
print(f"Valid private key: {valid_base58_key}")


from base58 import b58decode

def is_valid_base58(s):
    try:
        b58decode(s)
        return True
    except ValueError:
        return False

print(is_valid_base58(valid_base58_key))  # Should return True

# test_keygen.py
from solders.keypair import Keypair

keypair = Keypair()
print("\n🆕 TEST KEYPAIR (SAFE TO SHARE):")
print(f"PRIVATE_KEY={keypair}")
print("PUBKEY:", keypair.pubkey())