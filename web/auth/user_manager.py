import os
import json
import hashlib

from crypto.rsa_key import (
    generate_key_pair,
    save_private_key,
    save_public_key
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

USER_FILE = os.path.join(
BASE_DIR,
"database",
"users.json"
)

def load_users():

    try:

        with open(
            USER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return {}

def save_users(users):

    os.makedirs(
        os.path.dirname(USER_FILE),
        exist_ok=True
    )

    print("DATA TO SAVE:")
    print(users)

    with open(
        USER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4
        )

print("SAVE SUCCESS")


def hash_password(password):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

def register_user(username, password):

    users = load_users()

    if username in users:
        return False

    keys_dir = os.path.join(
        BASE_DIR,
        "keys"
    )

    os.makedirs(
        keys_dir,
        exist_ok=True
    )

    private_key_file = os.path.join(
        keys_dir,
        f"{username}_private.pem"
    )

    public_key_file = os.path.join(
        keys_dir,
        f"{username}_public.pem"
    )

    private_key, public_key = generate_key_pair()

    save_private_key(
        private_key,
        private_key_file
    )

    save_public_key(
        public_key,
        public_key_file
    )

    users[username] = {

        "password": hash_password(password),

        "private_key": private_key_file,

        "public_key": public_key_file

    }

    print("AFTER ADD USER:")
    print(users)

    save_users(users)

    return True

def login_user(username, password):

        users = load_users()

        if username not in users:

            return False

        return (
                users[username]["password"]
                ==
                hash_password(password)
            )