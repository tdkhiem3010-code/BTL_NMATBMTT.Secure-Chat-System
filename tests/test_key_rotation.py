from server.session_manager import SessionManager


manager = SessionManager()

session_id = manager.create_session(
    "Alice",
    "Bob"
)

for i in range(7):

    manager.increase_message_count(
        session_id
    )

    print(
        "Message",
        i + 1
    )

    if manager.need_rotation(
            session_id
    ):

        manager.rotate_session_key(
            session_id
        )
