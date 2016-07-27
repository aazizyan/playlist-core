from hashlib import sha256


LEASE_TIME = 480000


def hash_password(username, password):
    """
    Hashes username and password
    :param username: unique user name
    :param password: password
    :return: hash
    """
    pass_hash = sha256(password.encode()).digest()
    pass_hash = sha256(pass_hash + username.encode())
    return pass_hash.digest()
