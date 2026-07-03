from protocol.session import ChatSession
from crypto.key_exchange import generate_session_key
from crypto.key_exchange import encrypt_session_key
from crypto.rsa_key import load_public_key

print("SESSION MANAGER =", __file__)

class SessionManager:

    def __init__(self):

        self.sessions = {}

    def get_pair_key(
            self,
            user1,
            user2
    ):

        return tuple(
            sorted(
                [user1, user2]
            )
        )

    def create_session(
            self,
            user1,
            user2
    ):

        pair = self.get_pair_key(
            user1,
            user2
        )

        if pair in self.sessions:

            return self.sessions[pair]

        session = ChatSession()

        session_key = generate_session_key()

        self.sessions[pair] = {

            "session": session,

            "session_key": session_key,

            "encrypted_keys": {},

            "message_count": 0

        }

        return self.sessions[pair]

    def exchange_key(
            self,
            user,
            public_key_path,
            user1,
            user2
    ):

        session = self.get_session(
            user1,
            user2
        )

        public_key = load_public_key(
            public_key_path
        )

        encrypted_key = encrypt_session_key(

            session["session_key"],

            public_key

        )

        session["encrypted_keys"][user] = encrypted_key

        return encrypted_key

    def get_session(
            self,
            user1,
            user2
    ):

        pair = self.get_pair_key(
            user1,
            user2
        )

        if pair not in self.sessions:

            return self.create_session(
                user1,
                user2
            )

        return self.sessions[pair]

    def get_session_key(
            self,
            user1,
            user2
    ):

        return self.get_session(
            user1,
            user2
        )[
            "session_key"
        ]
    
    def set_encrypted_key(
            self,
            user1,
            user2,
            username,
            encrypted_key
    ):

        self.get_session(
            user1,
            user2
        )[
            "encrypted_keys"
        ][username] = encrypted_key

    def get_encrypted_key(
            self,
            user1,
            user2,
            username
    ):

        return self.get_session(
            user1,
            user2
        )[
            "encrypted_keys"
        ].get(username)

    def get_chat_session(
            self,
            user1,
            user2
    ):

        return self.get_session(
            user1,
            user2
        )[
            "session"
        ]

    def increase_message_count(
            self,
            user1,
            user2
    ):

        self.get_session(
            user1,
            user2
        )[
            "message_count"
        ] += 1

    def need_rotation(
            self,
            user1,
            user2
    ):

        return self.get_session(
            user1,
            user2
        )[
            "message_count"
        ] >= 5

    def rotate_session_key(
            self,
            user1,
            user2
    ):

        new_key = generate_session_key()

        session = self.get_session(
            user1,
            user2
        )

        session[
            "session_key"
        ] = new_key

        session[
            "message_count"
        ] = 0

        return new_key

import inspect

print("SESSION MANAGER =", __file__)
print("SIGNATURE =", inspect.signature(SessionManager.get_chat_session))