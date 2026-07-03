# 🔐 End-to-End Secure Text Chat v2 (Web-Based)

## FIT4012 – Network and Information Security

### Student Information

Nhóm 2
Họ và tên sinh viên:
1. Trần Đình Khiêm
2. La Văn Hải
3. Lương Như ý
4. Trương Văn Ban

---

# Project Overview

End-to-End Secure Text Chat v2 is a secure real-time web-based chat application developed as the final project for the Network and Information Security course.

The system demonstrates how modern cryptographic techniques can be integrated into a messaging application to provide:

- Confidentiality
- Integrity
- Authentication
- Replay attack protection
- Secure session key management

Unlike a traditional chat application, every message exchanged between users is protected using authenticated encryption and digital signatures before transmission.

The project also includes an interactive web interface that allows users to simulate common attacks in order to demonstrate how the implemented security mechanisms defend against them.

---

# Main Features

## User Authentication

- User Registration
- User Login
- Password hashing before storage
- Online user management

---

## Secure Communication

Each chat session includes:

- RSA-OAEP session key exchange
- AES-GCM authenticated encryption
- RSA digital signature
- Message authentication
- Message integrity verification

---

## Secure Message Packet

Every transmitted message contains:

- Message ID
- Session ID
- Sequence Number
- Timestamp
- Nonce
- Ciphertext
- Digital Signature

These fields are used to detect replay attacks and validate communication integrity.

---

## Replay Protection

The system prevents replay attacks using:

- Unique Message ID
- Sequence Number validation
- Replay Detector
- Packet registration

If an attacker replays an old packet, the system immediately detects and rejects it.

---

## Session Key Rotation

To reduce long-term key exposure, the application automatically rotates the AES session key after every five successfully transmitted messages.

Benefits:

- Forward secrecy simulation
- Reduced impact if one session key is compromised
- Demonstration of secure session lifecycle management

---

## Security Demonstration

The web interface includes multiple attack simulation modes.

### Valid Message

Normal encrypted communication.

Expected result:

VALID

---

### Replay Attack

Resends an already processed packet.

Expected result:


REPLAY ATTACK DETECTED

---

### Modify Ciphertext

Randomly modifies encrypted ciphertext.

Expected result:

INVALID SIGNATURE

or

DECRYPTION FAILED

---

### Modify Sequence Number

Changes the packet sequence number.

Expected result:

INVALID SEQUENCE

---

### Wrong Session Key

Attempts decryption using an incorrect AES session key.

Expected result:

DECRYPTION FAILED

---

### Fake Sender

Attempts to forge the sender identity.

Expected result:

INVALID SIGNATURE

---

# Security Technologies

| Component | Algorithm |
|-----------|-----------|
| Symmetric Encryption | AES-GCM |
| Session Key Exchange | RSA-OAEP |
| Digital Signature | RSA |
| Hash Function | SHA-256 |
| Replay Protection | Message ID + Sequence Number |
| Session Management | Automatic Key Rotation |

---

# Project Architecture

Browser A
      │
      │
Socket.IO
      │
      ▼
 Flask Web Server
      │
      │
Socket Handler
      │
      ├───────────────┐
      │               │
      ▼               ▼
Session Manager   Replay Detector
      │               │
      ▼               ▼
 Chat Engine     Packet Validation
      │
      ▼
 AES-GCM Encryption
      │
      ▼
 RSA Signature
      │
      ▼
 Browser B

---

# Project Structure

FIT4012-Secure-Chat
│
├── client/
├── crypto/
│   ├── aes_gcm.py
│   ├── rsa_encrypt.py
│   ├── rsa_signature.py
│   ├── rsa_key.py
│   └── key_exchange.py
│
├── protocol/
│   ├── packet.py
│   ├── session.py
│   └── message_processor.py
│
├── replay/
│   └── replay_detector.py
│
├── server/
│   └── session_manager.py
│
├── web/
│   ├── app.py
│   ├── websocket/
│   ├── security/
│   ├── auth/
│   ├── templates/
│   └── static/
│
├── tests/
├── docs/
├── diagram/
├── benchmark/
├── logs/
├── demo/
└── README.md

---

# Installation

Clone the repository:

bash
git clone <repository-url>
cd FIT4012-Secure-Chat

Install dependencies:

bash
pip install -r requirements.txt

---

# Run the Application

Start the Flask server:

bash
python web/app.py

or

bash
flask run

Open the browser:

http://127.0.0.1:5000

---

# Usage

1. Register two users.

2. Login.

3. Open chat.

4. Select another online user.

5. Send encrypted messages.

6. Observe the Security Information panel.

7. Enable attack simulation modes to verify security protections.

---

# Security Information Panel

For every message, the application displays:

- Plaintext
- AES Ciphertext
- Nonce
- RSA Signature
- Session ID
- Sequence Number
- Message ID
- Timestamp
- Security Status

This allows users to observe how each security mechanism operates in real time.

---

# Testing

The project includes security tests for:

- Valid Message
- Replay Attack
- Modify Ciphertext
- Modify Sequence Number
- Wrong Session Key
- Fake Sender
- Session Key Rotation

Screenshots and results are available in:


test_report/

---

# Documentation

Project documentation includes:

- Protocol Design
- Threat Model
- Test Report
- Benchmark Report
- Sequence Diagrams

Located in:

docs/
diagram/
benchmark/
test_report/

---

# Educational Purpose

This project is developed solely for educational purposes as part of the FIT4012 Network and Information Security course.

The implemented attack modes are demonstrations intended to illustrate how secure communication protocols defend against common attacks and should not be used for malicious activities.

---

# Future Improvements

Potential future enhancements include:

- Perfect Forward Secrecy using ECDH (X25519)
- Multi-user group chat
- Secure cloud key management
- Password hashing with Argon2 or bcrypt
- Database-backed user management
- TLS deployment
- Mobile client support

---

# Author

**Trần Khiêm**

FIT4012 – Network and Information Security

End-to-End Secure Text Chat v2