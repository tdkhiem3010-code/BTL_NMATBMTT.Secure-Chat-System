from dataclasses import dataclass
from datetime import datetime
import uuid
import json


@dataclass
class MessagePacket:

    message_id: str

    session_id: str

    sequence_number: int

    timestamp: str

    nonce: str

    sender: str

    ciphertext: str

    signature: str

    def to_dict(self):

        return {
            "message_id": self.message_id,
            "session_id": self.session_id,
            "sequence_number": self.sequence_number,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "sender": self.sender,
            "ciphertext": self.ciphertext,
            "signature": self.signature
        }

    def to_json(self):

        return json.dumps(
            self.to_dict()
        )

    @classmethod
    def from_json(cls, json_string):

        data = json.loads(
            json_string
        )

        return cls(**data)

    @classmethod
    def create(
            cls,
            session_id,
            sequence_number,
            sender,
            ciphertext="",
            signature=""
    ):

        return cls(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            sequence_number=sequence_number,
            timestamp=datetime.now().isoformat(),
            nonce=str(uuid.uuid4()),
            sender=sender,
            ciphertext=ciphertext,
            signature=signature
        )