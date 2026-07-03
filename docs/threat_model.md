# Threat Model

## Project

End-to-End Secure Text Chat v2

FIT4012 Secure System Upgrade Challenge

---

# 1. System Overview

The system enables two users to exchange text messages securely over an untrusted network.

Messages are encrypted using AES-GCM and authenticated using RSA digital signatures.

The system also provides replay attack protection and session key management.

---

# 2. Assets to Protect

The following assets must be protected:

| Asset            | Description                            |
| ---------------- | -------------------------------------- |
| Message Content  | Confidential text messages             |
| Session Key      | AES encryption key                     |
| Private Key      | RSA private key                        |
| Message Metadata | Session ID, sequence number, timestamp |
| Log Files        | Security event records                 |

---

# 3. Legitimate Users

### Alice

Authorized sender and receiver.

### Bob

Authorized sender and receiver.

### Server

Relays messages between participants.

The server is not trusted to read message content.

---

# 4. Potential Attackers

### Network Attacker

Can intercept packets transmitted over the network.

### Replay Attacker

Can resend previously captured packets.

### Impersonation Attacker

Attempts to forge messages pretending to be another user.

### Tampering Attacker

Attempts to modify encrypted messages during transmission.

---

# 5. Security Threats

## Threat 1: Eavesdropping

### Description

An attacker captures network traffic and attempts to read messages.

### Risk

Loss of confidentiality.

### Mitigation

AES-GCM encryption protects message content.

---

## Threat 2: Message Tampering

### Description

An attacker modifies ciphertext before delivery.

### Risk

Loss of integrity.

### Mitigation

AES-GCM authentication tag detects modifications.

RSA signature verification provides additional protection.

---

## Threat 3: Sender Impersonation

### Description

An attacker pretends to be a legitimate user.

### Risk

Unauthorized communication.

### Mitigation

RSA-PSS digital signatures authenticate the sender.

---

## Threat 4: Replay Attack

### Description

An attacker retransmits an old valid packet.

### Risk

Duplicate message processing.

### Mitigation

Message ID tracking.

Sequence number validation.

Replay detector.

---

## Threat 5: Session Key Exposure

### Description

Compromise of an old session key.

### Risk

Past or future message disclosure.

### Mitigation

Session key rotation after a predefined number of messages.

---

# 6. Security Objectives

## Confidentiality

Protect message content from unauthorized access.

## Integrity

Detect message modification.

## Authentication

Verify sender identity.

## Replay Protection

Prevent duplicate packet processing.

## Traceability

Record security events in log files.

---

# 7. Assumptions

* RSA private keys remain secret.
* The cryptography library is trusted.
* AES-GCM implementation is secure.
* Generated random values are unpredictable.
* End users protect their local systems.

---

# 8. Limitations

* No secure storage mechanism for private keys.
* No certificate authority infrastructure.
* No multi-user authentication server.
* No database integration.

---

# Conclusion

The implemented security controls mitigate the primary threats associated with secure text communication, including eavesdropping, tampering, replay attacks and sender impersonation.
