# Security Test Report

## Project

End-to-End Secure Text Chat v2

FIT4012 Secure System Upgrade Challenge

---

# Test Case 1: Valid Message

### Objective

Verify that a legitimate message can be encrypted, transmitted, authenticated and decrypted successfully.

### Expected Result

Receiver obtains the original plaintext.

### Result

PASS

---

# Test Case 2: Modified Ciphertext

### Objective

Verify that the system detects ciphertext tampering.

### Expected Result

Decryption fails and the modified message is rejected.

### Result

PASS

---

# Test Case 3: Modified Sequence Number

### Objective

Verify sequence number validation.

### Expected Result

The receiver rejects packets with invalid sequence numbers.

### Result

PASS

---

# Test Case 4: Replay Attack

### Objective

Verify replay attack protection.

### Expected Result

Duplicate packets are detected and rejected.

### Result

PASS

---

# Test Case 5: Wrong Session Key

### Objective

Verify behavior when the receiver uses an incorrect session key.

### Expected Result

Decryption fails.

### Result

PASS

---

# Test Case 6: Fake Sender

### Objective

Verify sender authentication using RSA digital signatures.

### Expected Result

Packets signed with an invalid private key are rejected.

### Result

PASS

---

# Test Case 7: Session Key Rotation

### Objective

Verify automatic session key update.

### Expected Result

Messages remain secure after key rotation.

### Result

PASS

---

# Summary

| Test Case                | Result |
| ------------------------ | ------ |
| Valid Message            | PASS   |
| Modified Ciphertext      | PASS   |
| Modified Sequence Number | PASS   |
| Replay Attack            | PASS   |
| Wrong Session Key        | PASS   |
| Fake Sender              | PASS   |
| Session Key Rotation     | PASS   |

---

All mandatory security tests required by the FIT4012 Secure System Upgrade Challenge were successfully completed.
