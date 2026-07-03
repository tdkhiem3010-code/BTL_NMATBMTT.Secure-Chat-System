from server.session_manager import SessionManager
from client.secure_chat_client import SecureChatClient
from protocol.session import ChatSession


manager = SessionManager()

session_id = manager.create_session(
    "Alice",
    "Bob"
)

session_key = manager.get_session_key(
    session_id
)


alice_session = ChatSession()
alice_session.session_id = session_id


bob_session = ChatSession()
bob_session.session_id = session_id


alice = SecureChatClient(
    "Alice",
    "keys/alice_private.pem",
    "keys/alice_public.pem",
    "keys/bob_public.pem",
    alice_session,
    session_key
)


bob = SecureChatClient(
    "Bob",
    "keys/bob_private.pem",
    "keys/bob_public.pem",
    "keys/alice_public.pem",
    bob_session,
    session_key
)


messages = [

    ("Alice", "Hello Bob"),

    ("Bob", "Hi Alice"),

    ("Alice", "How are you?"),

    ("Bob", "I'm fine"),

    ("Alice", "Nice to hear that"),

    ("Bob", "Session key rotation demo"),

    ("Alice", "Secure chat works"),

    ("Bob", "AES-GCM and RSA"),

    ("Alice", "Replay protection enabled"),

    ("Bob", "End of demo")

]


for sender, text in messages:

    if sender == "Alice":

        packet = alice.create_packet(
            text
        )

        plaintext = bob.receive_packet(
            packet
        )

        print()

        print(
            "Alice:",
            text
        )

        print(
            "Bob receives:",
            plaintext
        )

    else:

        packet = bob.create_packet(
            text
        )

        plaintext = alice.receive_packet(
            packet
        )

        print()

        print(
            "Bob:",
            text
        )

        print(
            "Alice receives:",
            plaintext
        )

    manager.increase_message_count(
        session_id
    )

    if manager.need_rotation(
            session_id
    ):

        new_key = manager.rotate_session_key(
            session_id
        )

        alice.update_session_key(
            new_key
        )

        bob.update_session_key(
            new_key
        )
