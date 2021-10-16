from pydantic import BaseSettings
import os
from functools import lru_cache
from cryptography.fernet import Fernet


mode = os.getenv("MODE", "local")

def decryption(message):
    '''복호화'''
    key = getKey()
    fernet = Fernet(key)

    return fernet.decrypt(message.encode("utf-8")).decode("utf-8")


@lru_cache()
def getKey():
    return os.getenv("fernet_key").encode("utf-8")


class GlobalSettings(BaseSettings):
    mode = mode


class LocalSettings(GlobalSettings):
    jenkins_host: str = decryption(
        "gAAAAABhantrQdkph22tUA15nqzg1pUxJFkSO8ykv9i3p3KhsUt2YOaun2Nyo-NEcLdkHB5q7J0mlY2mvJIpwi-DuryrK4R0gFmKjnwQqhQtB0ZmrMROew7PR4owXgx6Rcm73FU1zJno")
    jenkins_user: str = decryption(
        "gAAAAABhaonIXUqB2l6jQZHh4PYheQ4QCRl0Q-I3T9ShoxqVqFlxhaq9LK5G6RFhLeAqy0SVSlIIG-1lPjmqumjQhVbnI1spng=="
    )
    jenkins_password: str = decryption(
        "gAAAAABhaol-J20yARIPdl9MsiTYDYADSwqPW00au468KYN6IeWq_hx6CJkqZSVEgVxhS98dkTKfIdqaceYYEu1EWusw3H8aRZiVp9RmKzoH29jshAAndVyG3Am9d2horgfJ1NlpTnUY"
    )


class DevSettings(GlobalSettings):
    jenkins_host: str = decryption(
        "gAAAAABhaq7uutRglP5LIGboW_Ar-ig9DpRwnsTY4S2rK5JaBS5xoUpZnJm2uicKCJlmmoUP5Dj8ixsgrP1knQqXd5AKYj_P98JBGZhYDE0m8Ps3VYyOdzA=")
    jenkins_user: str = decryption(
        "gAAAAABhaonIXUqB2l6jQZHh4PYheQ4QCRl0Q-I3T9ShoxqVqFlxhaq9LK5G6RFhLeAqy0SVSlIIG-1lPjmqumjQhVbnI1spng=="
    )
    jenkins_password: str = decryption(
        "gAAAAABhaol-J20yARIPdl9MsiTYDYADSwqPW00au468KYN6IeWq_hx6CJkqZSVEgVxhS98dkTKfIdqaceYYEu1EWusw3H8aRZiVp9RmKzoH29jshAAndVyG3Am9d2horgfJ1NlpTnUY"
    )


@lru_cache()
def get_settings():
    if mode == "local":
        return LocalSettings()
    elif mode == "dev":
        return DevSettings()
