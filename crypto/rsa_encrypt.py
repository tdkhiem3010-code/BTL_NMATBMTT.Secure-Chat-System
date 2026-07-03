from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def encrypt_session_key(session_key, public_key):

    encrypted_key = public_key.encrypt(

        session_key,

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None
        )
    )

    return encrypted_key


def decrypt_session_key(encrypted_key, private_key):

    decrypted_key = private_key.decrypt(

        encrypted_key,

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None
        )
    )

    return decrypted_key