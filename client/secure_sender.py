from protocol.message_processor import MessageProcessor
from logs.logger import log_event


class SecureSender:

    def __init__(
            self,
            sender_name,
            session,
            session_key,
            private_key
    ):

        self.sender_name = sender_name
        self.session = session
        self.session_key = session_key
        self.private_key = private_key

    def send_message(self, plaintext):

        packet = MessageProcessor.create_packet(
            plaintext=plaintext,
            session=self.session,
            sender=self.sender_name,
            session_key=self.session_key,
            private_key=self.private_key
        )

        log_event(
            f"{self.sender_name} SEND MESSAGE seq={packet.sequence_number}"
        )

        return packet
    def update_session_key(
            self,
            new_session_key
    ):

        self.session_key = new_session_key