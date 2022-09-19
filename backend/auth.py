# authorisation via sha256
import hashlib

SALT = b'\xbd|h\x13\xeezf\xa2\xc14\xe0\xf0\x92\xa1V\x8b'


class Auth:
    @staticmethod
    def hash_pass(password):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 10000, dklen=64)

    @staticmethod
    def check_pass(newPassword, password):
        if Auth.hash_pass(newPassword) == password:
            return True
        else:
            return False
