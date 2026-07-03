class ReplayDetector:

    def __init__(self):

        self.processed_message_ids = set()

        self.last_sequence_numbers = {}

    def is_replay(self, packet):

        if packet.message_id in self.processed_message_ids:

            return True

        if not self.is_valid_sequence(packet):

            return True

        return False

    def is_valid_sequence(self, packet):

        sender = packet.sender

        if sender not in self.last_sequence_numbers:

            expected = 1

        else:

            expected = (
                self.last_sequence_numbers[sender]
                + 1
            )

        return packet.sequence_number == expected

    def register_packet(self, packet):

        self.processed_message_ids.add(
            packet.message_id
        )

        self.last_sequence_numbers[
            packet.sender
        ] = packet.sequence_number
        