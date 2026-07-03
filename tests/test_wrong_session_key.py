from server.session_manager import SessionManager
from client.secure_chat_client import SecureChatClient
from crypto.key_exchange import generate_session_key


manager = SessionManager()

session_id = manager.create_session(
    "Alice",
    "Bob"
)

session = manager.get_chat_session(
    session_id
)

correct_session_key = manager.get_session_key(
    session_id
)

wrong_session_key = generate_session_key()


alice = SecureChatClient(
    "Alice",
    "keys/alice_private.pem",
    "keys/alice_public.pem",
    "keys/bob_public.pem",
    session,
    correct_session_key
)

bob = SecureChatClient(
    "Bob",
    "keys/bob_private.pem",
    "keys/bob_public.pem",
    "keys/alice_public.pem",
    session,
    wrong_session_key
)


packet = alice.create_packet(
    "Hello Bob"
)


try:

    message = bob.receive_packet(
        packet
    )

    print(message)

except Exception:

    print()

    print("WRONG SESSION KEY")

    print("PASS")