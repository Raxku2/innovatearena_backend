import requests
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
from os import getenv, urandom
import secrets
import hashlib
import base64

load_dotenv()


PASSWORD = getenv("FA_PASSWORD")
USER = getenv("FA_USERNAME")
security = HTTPBasic()


def authenticate(cred: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(cred.username, USER)
    correct_password = match_hash(cred.password)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return cred.username


def handle_success(access_token: str) -> dict | None:
    try:
        url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # raises error if status != 200

        data = response.json()
        print("User Authenticated:", data)
        return data

    except requests.exceptions.RequestException as error:
        print("Profile fetch failed:", error)
        return None


def generate_hash(text: str) -> str:
    salt = urandom(16)  # random salt
    key = hashlib.pbkdf2_hmac(
        "sha256",
        text.encode("utf-8"),
        salt,
        200000,  # iterations (slow = harder to brute force)
    )

    # Return the salt + key concatenated, base64 encoded
    return base64.b64encode(salt + key).decode("utf-8")


def match_hash(text: str) -> bool:
    # Decode the stored hash (salt + key)
    data = base64.b64decode(PASSWORD)
    salt = data[:16]  # Extract salt (first 16 bytes)
    stored_key = data[16:]  # Extract stored hashed password (rest of the bytes)

    # Hash the input text with the same salt using PBKDF2
    new_key = hashlib.pbkdf2_hmac(
        "sha256",
        text.encode("utf-8"),
        salt,
        200000,  # Same number of iterations as during hash creation
    )

    # Return True if the hashes match, otherwise False
    return new_key == stored_key
