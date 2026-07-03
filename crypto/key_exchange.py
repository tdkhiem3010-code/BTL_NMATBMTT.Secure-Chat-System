import secrets

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def generate_session_key():

    return secrets.token_bytes(32)


def encrypt_session_key(
        session_key,
        public_key
):

    return public_key.encrypt(

        session_key,

        padding.OAEP(

            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None

        )

    )


def decrypt_session_key(
        encrypted_key,
        private_key
):

    return private_key.decrypt(

        encrypted_key,

        padding.OAEP(

            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None

        )

    )