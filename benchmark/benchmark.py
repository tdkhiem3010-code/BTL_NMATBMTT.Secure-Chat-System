import time

from crypto.key_exchange import generate_session_key
from crypto.aes_gcm import encrypt_message, decrypt_message

from crypto.rsa_key import (
    load_private_key,
    load_public_key
)

from crypto.rsa_signature import (
    sign_message,
    verify_signature
)


private_key = load_private_key(
    "keys/alice_private.pem"
)

public_key = load_public_key(
    "keys/alice_public.pem"
)

session_key = generate_session_key()

plaintext = "Hello Secure Chat"


# ==========================
# AES-GCM Encryption
# ==========================
start = time.perf_counter()

for _ in range(1000):

    nonce, ciphertext = encrypt_message(
        session_key,
        plaintext
    )

end = time.perf_counter()

aes_encrypt_time = (
    end - start
) / 1000


# ==========================
# AES-GCM Decryption
# ==========================
start = time.perf_counter()

for _ in range(1000):

    decrypt_message(
        session_key,
        nonce,
        ciphertext
    )

end = time.perf_counter()

aes_decrypt_time = (
    end - start
) / 1000


# ==========================
# RSA Signature
# ==========================
message_bytes = plaintext.encode()

start = time.perf_counter()

for _ in range(100):

    signature = sign_message(
        message_bytes,
        private_key
    )

end = time.perf_counter()

sign_time = (
    end - start
) / 100


# ==========================
# RSA Verify
# ==========================
start = time.perf_counter()

for _ in range(100):

    verify_signature(
        message_bytes,
        signature,
        public_key
    )

end = time.perf_counter()

verify_time = (
    end - start
) / 100


# ==========================
# Output
# ==========================
print()
print("===== BENCHMARK RESULT =====")
print()

print(
    f"AES-GCM Encrypt : {aes_encrypt_time:.8f} seconds"
)

print(
    f"AES-GCM Decrypt : {aes_decrypt_time:.8f} seconds"
)

print(
    f"RSA Sign        : {sign_time:.8f} seconds"
)

print(
    f"RSA Verify      : {verify_time:.8f} seconds"
)

print()
print("Benchmark completed.")