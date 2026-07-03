from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def encrypt_message(session_key, plaintext):

    aesgcm = AESGCM(session_key)

    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(
        nonce,
        plaintext.encode(),
        None
    )

    return nonce, ciphertext


def decrypt_message(session_key, nonce, ciphertext):

    aesgcm = AESGCM(session_key)

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode()