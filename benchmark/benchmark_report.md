# BENCHMARK REPORT

## Project

End-to-End Secure Text Chat v2

---

# Environment

- Python 3.13
- cryptography library
- Windows 11
- Intel CPU

---

# ===== BENCHMARK RESULT =====

AES-GCM Encrypt : 0.00000579 seconds
AES-GCM Decrypt : 0.00000573 seconds
RSA Sign        : 0.00086808 seconds
RSA Verify      : 0.00008761 seconds
---

# Analysis

AES-GCM encryption and decryption are very fast and suitable for message transmission.

RSA-PSS operations are slower than AES-GCM, but their performance is acceptable because RSA is only used for authentication and session key exchange.

The benchmark results indicate that the system can provide confidentiality, integrity and authentication while maintaining acceptable performance.

---

# Conclusion

The secure chat system demonstrates good performance and is suitable for secure text communication.
