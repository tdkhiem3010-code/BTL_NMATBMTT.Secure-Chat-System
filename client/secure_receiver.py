from protocol.message_processor import MessageProcessor
from replay.replay_detector import ReplayDetector
from logs.logger import log_event


class SecureReceiver:

    def __init__(
            self,
            session_key,
            sender_public_key
    ):

        self.session_key = session_key
        self.sender_public_key = sender_public_key

        self.replay_detector = ReplayDetector()

    def receive_message(self, packet):

        if self.replay_detector.is_replay(packet):

            log_event(
                "REPLAY ATTACK DETECTED"
            )

            return None

        if not self.replay_detector.is_valid_sequence(packet):

            log_event(
                "INVALID SEQUENCE NUMBER"
            )

            return None

        self.replay_detector.register_packet(
            packet
        )

        plaintext, valid = MessageProcessor.process_packet(
            packet,
            self.session_key,
            self.sender_public_key
        )

        if not valid:

            log_event(
                "INVALID SIGNATURE"
            )

            return None

        log_event(
            f"RECEIVE MESSAGE seq={packet.sequence_number}"
        )

        return plaintext
    def update_session_key(
            self,
            new_session_key
    ):

        self.session_key = new_session_key