# Protocol Design

## Project

End-to-End Secure Text Chat v2

FIT4012 Secure System Upgrade Challenge

---

# 1. Overview

The system provides secure end-to-end text communication between two users.

Each message is encrypted using AES-GCM and authenticated using RSA digital signatures.

Additional security mechanisms include replay attack detection and session key rotation.

---

# 2. Communication Participants

### Alice

Legitimate sender and receiver.

### Bob

Legitimate sender and receiver.

### Server

Message relay component.

The server does not have access to plaintext messages.

---

# 3. Message Packet Structure

Each transmitted packet contains:

| Field           | Description               |
| --------------- | ------------------------- |
| message_id      | Unique message identifier |
| session_id      | Chat session identifier   |
| sequence_number | Message sequence number   |
| timestamp       | Packet creation time      |
| nonce           | AES-GCM nonce             |
| sender          | Sender identity           |
| ciphertext      | Encrypted message         |
| signature       | RSA digital signature     |

---

# 4. Message Sending Procedure

### Step 1

The sender enters plaintext.

---

### Step 2

The plaintext is digitally signed using RSA-PSS.

Result:

Signature

---

### Step 3

The plaintext is encrypted using AES-GCM with the current session key.

Result:

Nonce

Ciphertext

Authentication tag

---

### Step 4

A MessagePacket object is created.

The packet contains:

* message_id
* session_id
* sequence_number
* timestamp
* nonce
* sender
* ciphertext
* signature

---

### Step 5

The packet is transmitted to the receiver.

---

# 5. Message Receiving Procedure

### Step 1

The receiver obtains the packet.

---

### Step 2

ReplayDetector checks:

* message_id
* sequence_number

Replay packets are rejected.

---

### Step 3

AES-GCM decrypts the ciphertext.

---

### Step 4

RSA-PSS verifies the digital signature.

---

### Step 5

If verification succeeds, plaintext is delivered to the user.

Otherwise, the packet is discarded.

---

# 6. Replay Protection

The ReplayDetector maintains:

* processed_message_ids
* last_sequence_number

Protection mechanisms:

* message_id uniqueness
* sequence number validation

Duplicate packets are rejected.

---

# 7. Session Key Rotation

The SessionManager maintains:

* session_key
* message_count

After a predefined number of messages:

1. Generate a new session key.
2. Replace the previous key.
3. Reset message counter.
4. Continue communication with the new key.

This limits the impact of session key compromise.

---

# 8. Logging

Security events are recorded in chat.log.

Logged events include:

* Message sending
* Message receiving
* Signature verification
* Replay detection
* Invalid sequence number
* Session key rotation

Sensitive information such as plaintext messages, passwords and secret keys are not stored.

---

# 9. UML Sequence Diagrams

The following UML sequence diagrams describe the protocol:

### secure_chat_sequence

Normal secure communication.

---

### replay_attack_sequence

Replay attack detection.

---

### key_rotation_sequence

Session key update process.

---

# Conclusion

The designed protocol provides:

* Confidentiality
* Integrity
* Authentication
* Replay protection
* Traceability

through the combined use of AES-GCM, RSA-PSS, replay detection and session key rotation.
