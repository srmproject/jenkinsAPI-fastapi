from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os
import pytest


@pytest.mark.skip
def test_encode():
    '''
    데이터 암호화&복호화 테스트
    실행방법: python -m pytest tests/test_encryption_config.py::test_encode -s
    참고자료: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
    '''
    message = ""
    key = getKey()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode("utf-8"))

    print("key: ", key)
    print("original string: ", message)
    print("encrypted string: ", encMessage)

    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)


@pytest.mark.skip
def test_encryption():
    '''
    데이터 복호화 테스트
    실행방법: python -m pytest tests/test_encryption_config.py::test_encryption -s
    참고자료: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
    '''
    message = ""
    key = "".encode("utf-8")
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode("utf-8"))

    print("key: ", key)
    print("original string: ", encMessage)


@pytest.mark.skip
def test_decryption():
    '''
    데이터 복호화 테스트
    실행방법: python -m pytest tests/test_encryption_config.py::test_decryption -s
    참고자료: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
    '''
    key = "".encode("utf-8")
    fernet = Fernet(key)

    encMessage = "".encode("utf-8")
    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)


def getKey():
    password = "password".encode("utf-8")
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password))
