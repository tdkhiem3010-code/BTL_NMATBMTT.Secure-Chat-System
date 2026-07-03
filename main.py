from server.session_manager import SessionManager
from client.secure_chat_client import SecureChatClient


def main():

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

    print()
    print("===== SECURE CHAT DEMO =====")
    print()

    # Alice -> Bob

    print("Alice gửi:")
    print("Hello Bob")

    packet1 = alice.create_packet(
        "Hello Bob"
    )

    message1 = bob.receive_packet(
        packet1
    )

    print()

    print("Bob nhận:")
    print(message1)

    print()
    print("----------------------------")
    print()

    # Bob -> Alice

    print("Bob gửi:")
    print("Hello Alice")

    packet2 = bob.create_packet(
        "Hello Alice"
    )

    message2 = alice.receive_packet(
        packet2
    )

    print()

    print("Alice nhận:")
    print(message2)


if __name__ == "__main__":
    main()
