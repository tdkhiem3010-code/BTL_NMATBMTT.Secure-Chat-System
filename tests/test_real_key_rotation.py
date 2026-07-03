from server.session_manager import SessionManager
from client.secure_chat_client import SecureChatClient


manager = SessionManager()

session_id = manager.create_session(
    "Alice",
    "Bob"
)

session = manager.get_chat_session(
    session_id
)

session_key = manager.get_session_key(
    session_id
)

alice = SecureChatClient(
    "Alice",
    "keys/alice_private.pem",
    "keys/alice_public.pem",
    "keys/bob_public.pem",
    session,
    session_key
)

bob = SecureChatClient(
    "Bob",
    "keys/bob_private.pem",
    "keys/bob_public.pem",
    "keys/alice_public.pem",
    session,
    session_key
)


for i in range(10):

    packet = alice.create_packet(
        f"Message {i+1}"
    )

    message = bob.receive_packet(
        packet
    )

    print(
        "Bob nhận:",
        message
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
