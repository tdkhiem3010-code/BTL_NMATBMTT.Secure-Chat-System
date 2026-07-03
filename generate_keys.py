from crypto.rsa_key import (
    generate_key_pair,
    save_private_key,
    save_public_key
)


# Alice

alice_private, alice_public = generate_key_pair()

save_private_key(
    alice_private,
    "keys/alice_private.pem"
)

save_public_key(
    alice_public,
    "keys/alice_public.pem"
)


# Bob

bob_private, bob_public = generate_key_pair()

save_private_key(
    bob_private,
    "keys/bob_private.pem"
)

save_public_key(
    bob_public,
    "keys/bob_public.pem"
)

print("Tạo khóa thành công")