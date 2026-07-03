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
    username="Alice",
    private_key_path="keys/alice_private.pem",
    public_key_path="keys/alice_public.pem",
    peer_public_key_path="keys/bob_public.pem",
    session=session,
    session_key=session_key
)

bob = SecureChatClient(
    username="Bob",
    private_key_path="keys/bob_private.pem",
    public_key_path="keys/bob_public.pem",
    peer_public_key_path="keys/alice_public.pem",
    session=session,
    session_key=session_key
)

packet = alice.create_packet(
    "Hello Bob"
)

message = bob.receive_packet(
    packet
)

print()

print("Bob nhận được:")

print(message)
