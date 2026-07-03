from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_key_pair():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def save_private_key(private_key, filename):

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(filename, "wb") as file:
        file.write(pem)


def save_public_key(public_key, filename):

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(filename, "wb") as file:
        file.write(pem)


def load_private_key(filename):

    with open(filename, "rb") as file:

        return serialization.load_pem_private_key(
            file.read(),
            password=None
        )


def load_public_key(filename):

    with open(filename, "rb") as file:

        return serialization.load_pem_public_key(
            file.read()
        )