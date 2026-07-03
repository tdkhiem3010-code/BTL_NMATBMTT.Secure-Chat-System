from client.secure_sender import SecureSender
from client.secure_receiver import SecureReceiver

from crypto.rsa_key import (
    load_private_key,
    load_public_key
)


class SecureChatClient:

    def __init__(
            self,
            username,
            private_key_path,
            public_key_path,
            peer_public_key_path,
            session,
            session_key
    ):

        self.username = username

        self.private_key = load_private_key(
            private_key_path
        )

        self.public_key = load_public_key(
            public_key_path
        )

        self.peer_public_key = load_public_key(
            peer_public_key_path
        )

        self.session = session

        self.session_key = session_key

        self.sender = SecureSender(
            sender_name=username,
            session=session,
            session_key=session_key,
            private_key=self.private_key
        )

        self.receiver = SecureReceiver(
            session_key=session_key,
            sender_public_key=self.peer_public_key
        )

    def create_packet(self, plaintext):

        return self.sender.send_message(
            plaintext
        )

    def receive_packet(self, packet):

        return self.receiver.receive_message(
            packet
        )
    def update_session_key(
            self,
            new_session_key
    ):

        self.session_key = new_session_key

        self.sender.update_session_key(
            new_session_key
        )

        self.receiver.update_session_key(
            new_session_key
        )