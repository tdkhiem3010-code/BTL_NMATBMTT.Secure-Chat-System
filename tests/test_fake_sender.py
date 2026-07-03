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


packet = alice.create_packet(
    "Hello Bob"
)

packet.signature = "AAAA"


message = bob.receive_packet(
    packet
)

print()

if message is None:

    print("INVALID SIGNATURE")

    print("PASS")

else:

    print("FAIL")
