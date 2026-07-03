from flask_socketio import emit
import base64

from flask import session
from flask import request

from crypto.aes_gcm import encrypt_message
from crypto.aes_gcm import decrypt_message

from crypto.rsa_key import load_private_key
from crypto.rsa_key import load_public_key

from crypto.rsa_signature import sign_message
from crypto.rsa_signature import verify_signature

from crypto.key_exchange import encrypt_session_key
from crypto.key_exchange import generate_session_key
from replay.replay_detector import ReplayDetector

from crypto.key_exchange import decrypt_session_key
from server.session_manager import SessionManager

from protocol.packet import MessagePacket

from logs.logger import log_event


manager = SessionManager()

replay_detector = ReplayDetector()

online_users = {}

user_sids = {}

last_packet = None

last_context = {}

ATTACK_MODIFIED_CIPHERTEXT = False

ATTACK_SEQUENCE = False

ATTACK_WRONG_KEY = False

ATTACK_FAKE_SENDER = False


def _attack_mode_state():

    return {
        "ciphertext": ATTACK_MODIFIED_CIPHERTEXT,
        "sequence": ATTACK_SEQUENCE,
        "wrong_key": ATTACK_WRONG_KEY,
        "fake_sender": ATTACK_FAKE_SENDER
    }


def _build_message_data(
        sender,
        receiver,
        packet,
        plaintext,
        encrypted_session_key,
        security_status
):

    return {
        "sender": sender,
        "receiver": receiver,
        "encrypted_session_key": base64.b64encode(
            encrypted_session_key
        ).decode(),
        "plaintext": plaintext,
        "ciphertext": packet.ciphertext,
        "nonce": packet.nonce,
        "signature": packet.signature,
        "session_id": packet.session_id,
        "sequence_number": packet.sequence_number,
        "message_id": packet.message_id,
        "timestamp": packet.timestamp,
        "security_status": security_status
    }


def _emit_message(socketio, sender, receiver, message_data):

    receiver_sid = user_sids.get(receiver)

    if receiver_sid:

        socketio.emit(
            "receive_message",
            message_data,
            to=receiver_sid
        )

    sender_sid = user_sids.get(sender)

    if sender_sid:

        socketio.emit(
            "receive_message",
            message_data,
            to=sender_sid
        )


def register_socket_events(socketio):

    @socketio.on("connect")
    def handle_connect():

        username = session.get("username")

        if username is None:

            return

        online_users[request.sid] = username

        user_sids[username] = request.sid

        print(username, "CONNECTED")

        emit(
            "online_users",
            list(online_users.values()),
            broadcast=True
        )

        emit(
            "attack_mode",
            _attack_mode_state()
        )

    @socketio.on("disconnect")
    def handle_disconnect():

        if request.sid not in online_users:

            return

        username = online_users[request.sid]

        print(username, "DISCONNECTED")

        del online_users[request.sid]

        if username in user_sids:

            del user_sids[username]

        emit(
            "online_users",
            list(online_users.values()),
            broadcast=True
        )

    @socketio.on("send_message")
    def handle_message(data):

        global last_packet, last_context

        sender = session["username"]
        receiver = data["receiver"]
        message = data["message"]

        sender_private_key = load_private_key(
            f"web/keys/{sender}_private.pem"
        )

        sender_public_key = load_public_key(
            f"web/keys/{sender}_public.pem"
        )

        chat_session = manager.get_chat_session(
            sender,
            receiver
        )

        session_key = manager.get_session_key(
            sender,
            receiver
        )

        receiver_public_key = load_public_key(
            f"web/keys/{receiver}_public.pem"
        )

        encrypted_session_key = encrypt_session_key(
            session_key,
            receiver_public_key
        )

        receiver_private_key = load_private_key(
            f"web/keys/{receiver}_private.pem"
        )

        decrypted_session_key = decrypt_session_key(
            encrypted_session_key,
            receiver_private_key
        )

        if decrypted_session_key == session_key:
            print("RSA-OAEP Key Exchange: SUCCESS")
            log_event("RSA-OAEP Key Exchange: SUCCESS")
        else:
            print("RSA-OAEP Key Exchange: FAILED")
            log_event("RSA-OAEP Key Exchange: FAILED")

        manager.set_encrypted_key(
            sender,
            receiver,
            receiver,
            encrypted_session_key
        )

        if sender in replay_detector.last_sequence_numbers:

            next_seq = (
                replay_detector.last_sequence_numbers[sender]
                + 1
            )

        else:

            next_seq = 1

        packet = MessagePacket.create(
            session_id=chat_session.session_id,
            sequence_number=next_seq,
            sender=sender
        )

        if ATTACK_SEQUENCE:

            print("ATTACK: MODIFY SEQUENCE")
            log_event("ATTACK: MODIFY SEQUENCE")

            packet.sequence_number += 5

        if packet.message_id in replay_detector.processed_message_ids:

            print("REPLAY ATTACK DETECTED")
            log_event("REPLAY ATTACK DETECTED")

            message_data = _build_message_data(
                sender,
                receiver,
                packet,
                "[REPLAY ATTACK DETECTED]",
                encrypted_session_key,
                "REPLAY ATTACK DETECTED"
            )

            _emit_message(
                socketio,
                sender,
                receiver,
                message_data
            )

            return

        if not replay_detector.is_valid_sequence(packet):

            print("INVALID SEQUENCE DETECTED")
            log_event("INVALID SEQUENCE NUMBER")

            message_data = _build_message_data(
                sender,
                receiver,
                packet,
                "[INVALID SEQUENCE]",
                encrypted_session_key,
                "INVALID SEQUENCE"
            )

            _emit_message(
                socketio,
                sender,
                receiver,
                message_data
            )

            return

        signature = sign_message(
            message.encode(),
            sender_private_key
        )

        log_event(
            f"{sender} ENCRYPTION seq={packet.sequence_number}"
        )

        nonce, ciphertext = encrypt_message(
            session_key,
            message
        )

        packet.ciphertext = base64.b64encode(
            ciphertext
        ).decode()

        if ATTACK_MODIFIED_CIPHERTEXT:

            print("ATTACK: MODIFY CIPHERTEXT")
            log_event("ATTACK: MODIFY CIPHERTEXT")

            temp = bytearray(ciphertext)

            temp[0] ^= 0xFF

            ciphertext = bytes(temp)

            packet.ciphertext = base64.b64encode(
                ciphertext
            ).decode()

        packet.nonce = base64.b64encode(
            nonce
        ).decode()

        packet.signature = base64.b64encode(
            signature
        ).decode()

        if ATTACK_FAKE_SENDER:

            print("ATTACK: FAKE SENDER")
            log_event("ATTACK: FAKE SENDER")

            packet.signature = "AAAA"

        decrypt_key = session_key

        if ATTACK_WRONG_KEY:

            print("ATTACK: WRONG SESSION KEY")
            log_event("ATTACK: WRONG SESSION KEY")

            decrypt_key = generate_session_key()

        plaintext = message
        security_status = "VALID"

        try:

            plaintext = decrypt_message(
                decrypt_key,
                nonce,
                ciphertext
            )

            log_event(
                f"{sender} DECRYPTION seq={packet.sequence_number}"
            )

        except Exception:

            print("DECRYPT FAILED")
            log_event("DECRYPT FAILED")

            if ATTACK_WRONG_KEY:

                plaintext = "[WRONG SESSION KEY]"

                security_status = "WRONG SESSION KEY"

            else:

                plaintext = "[CIPHERTEXT MODIFIED]"

                security_status = "CIPHERTEXT MODIFIED"

        try:

            sig_bytes = base64.b64decode(
                packet.signature
            )

            valid = verify_signature(
                plaintext.encode(),
                sig_bytes,
                sender_public_key
            )

        except Exception:

            valid = False

        if valid:
            print("Digital Signature: VERIFIED")
            log_event("Digital Signature: VERIFIED")
        else:
            print("Digital Signature: INVALID")
            log_event("INVALID SIGNATURE")

            if ATTACK_FAKE_SENDER:

                plaintext = "[INVALID SIGNATURE]"

                security_status = "INVALID SIGNATURE"

            elif security_status == "VALID":

                security_status = "INVALID SIGNATURE"

        if security_status == "VALID":

            replay_detector.register_packet(
                packet
            )

            last_packet = packet

            last_context = {
                "sender": sender,
                "receiver": receiver,
                "encrypted_session_key": encrypted_session_key
            }

        message_data = _build_message_data(
            sender,
            receiver,
            packet,
            plaintext,
            encrypted_session_key,
            security_status
        )

        _emit_message(
            socketio,
            sender,
            receiver,
            message_data
        )

        if security_status == "VALID":

            manager.increase_message_count(
                sender,
                receiver
            )

            if manager.need_rotation(
                sender,
                receiver
            ):

                print("ROTATING SESSION KEY...")
                log_event("SESSION KEY ROTATION")

                manager.rotate_session_key(
                    sender,
                    receiver
                )

                new_key = manager.get_session_key(
                    sender,
                    receiver
                )

                encrypted_key = encrypt_session_key(
                    new_key,
                    receiver_public_key
                )

                receiver_sid = user_sids.get(receiver)

                emit(
                    "session_rotated",
                    {
                        "receiver": receiver,
                        "encrypted_session_key":
                            base64.b64encode(
                                encrypted_key
                            ).decode()
                    },
                    to=receiver_sid
                )

                emit(
                    "session_rotated",
                    {
                        "receiver": receiver,
                        "encrypted_session_key":
                            base64.b64encode(
                                encrypted_key
                            ).decode()
                    },
                    to=request.sid
                )

                print("NEW SESSION KEY GENERATED")
                log_event("NEW SESSION KEY GENERATED")

    @socketio.on("disable_attacks")
    def disable_attacks():

        global ATTACK_MODIFIED_CIPHERTEXT
        global ATTACK_SEQUENCE
        global ATTACK_WRONG_KEY
        global ATTACK_FAKE_SENDER

        ATTACK_MODIFIED_CIPHERTEXT = False
        ATTACK_SEQUENCE = False
        ATTACK_WRONG_KEY = False
        ATTACK_FAKE_SENDER = False

        print("ATTACK MODE: ALL OFF (NORMAL MESSAGE)")
        log_event("ATTACK MODE: ALL OFF")

        emit(
            "attack_mode",
            _attack_mode_state()
        )

    @socketio.on("toggle_ciphertext_attack")
    def toggle_ciphertext_attack():

        global ATTACK_MODIFIED_CIPHERTEXT

        ATTACK_MODIFIED_CIPHERTEXT = not ATTACK_MODIFIED_CIPHERTEXT

        print(
            "CIPHERTEXT ATTACK MODE =",
            ATTACK_MODIFIED_CIPHERTEXT
        )

        emit(
            "attack_mode",
            _attack_mode_state()
        )

    @socketio.on("toggle_sequence_attack")
    def toggle_sequence_attack():

        global ATTACK_SEQUENCE

        ATTACK_SEQUENCE = not ATTACK_SEQUENCE

        print(
            "SEQUENCE ATTACK MODE =",
            ATTACK_SEQUENCE
        )

        emit(
            "attack_mode",
            _attack_mode_state()
        )

    @socketio.on("toggle_wrong_key_attack")
    def toggle_wrong_key_attack():

        global ATTACK_WRONG_KEY

        ATTACK_WRONG_KEY = not ATTACK_WRONG_KEY

        print(
            "WRONG KEY ATTACK MODE =",
            ATTACK_WRONG_KEY
        )

        emit(
            "attack_mode",
            _attack_mode_state()
        )

    @socketio.on("toggle_fake_sender")
    def toggle_fake_sender():

        global ATTACK_FAKE_SENDER

        ATTACK_FAKE_SENDER = not ATTACK_FAKE_SENDER

        print(
            "FAKE SENDER ATTACK MODE =",
            ATTACK_FAKE_SENDER
        )

        emit(
            "attack_mode",
            _attack_mode_state()
        )

    @socketio.on("replay_attack")
    def handle_replay_attack():

        global last_packet, last_context

        if last_packet is None:

            print("NO PACKET")
            log_event("REPLAY ATTACK: NO PACKET")

            emit(
                "security_alert",
                {
                    "message": "NO PACKET TO REPLAY"
                }
            )

            return

        sender = last_context.get("sender")

        receiver = last_context.get("receiver")

        encrypted_session_key = last_context.get(
            "encrypted_session_key"
        )

        if replay_detector.is_replay(last_packet):

            print("Replay Attack Detected")
            print(f"Message ID: {last_packet.message_id}")
            log_event("REPLAY ATTACK DETECTED")

            message_data = _build_message_data(
                sender,
                receiver,
                last_packet,
                "[REPLAY ATTACK DETECTED]",
                encrypted_session_key,
                "REPLAY ATTACK DETECTED"
            )

            _emit_message(
                socketio,
                sender,
                receiver,
                message_data
            )

        else:

            print("REPLAY CHECK: PACKET NOT DUPLICATE")
            log_event("REPLAY CHECK: NOT DUPLICATE")

            emit(
                "security_alert",
                {
                    "message": "PACKET NOT YET REGISTERED"
                }
            )
