import uuid


class ChatSession:

    def __init__(self):

        self.session_id = str(uuid.uuid4())

        self.sequence_number = 0

    def next_sequence_number(self):

        self.sequence_number += 1

        return self.sequence_number