import base64

from protocol.packet import MessagePacket

from crypto.aes_gcm import (
    encrypt_message,
    decrypt_message
)

from crypto.rsa_signature import (
    sign_message,
    verify_signature
)


class MessageProcessor:

    @staticmethod
    def create_packet(
            plaintext,
            session,
            sender,
            session_key,
            private_key
    ):

        message_bytes = plaintext.encode()

        signature = sign_message(
            message_bytes,
            private_key
        )

        nonce, ciphertext = encrypt_message(
            session_key,
            plaintext
        )

        packet = MessagePacket.create(
            session_id=session.session_id,
            sequence_number=session.next_sequence_number(),
            sender=sender,
            ciphertext=base64.b64encode(ciphertext).decode(),
            signature=base64.b64encode(signature).decode()
        )

        packet.nonce = base64.b64encode(
            nonce
        ).decode()

        return packet

    @staticmethod
    def process_packet(
            packet,
            session_key,
            sender_public_key
    ):

        nonce = base64.b64decode(
            packet.nonce
        )

        ciphertext = base64.b64decode(
            packet.ciphertext
        )

        signature = base64.b64decode(
            packet.signature
        )

        plaintext = decrypt_message(
            session_key,
            nonce,
            ciphertext
        )

        valid = verify_signature(
            plaintext.encode(),
            signature,
            sender_public_key
        )

        return plaintext, valid