import jwt
from cryptography.hazmat.primitives import serialization


class AuthClient:
    _signing_key: serialization.SSHPrivateKeyTypes | None

    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key
        self._signing_key = None

    @property
    def signing_key(self) -> serialization.SSHPrivateKeyTypes:
        if self._signing_key:
            return self._signing_key
        self._signing_key = serialization.load_ssh_private_key(self.private_key.encode(), password=b'')
        return self._signing_key

    def create_access_token(self, user_id: str) -> dict:
        token = jwt.encode(payload={'sub': user_id}, key=str(self.signing_key))
        return {'access_token': token, 'token_type': 'bearer'}

    def decode_token(self, token: str) -> dict:
        header = jwt.get_unverified_header(token)
        algorithm = header.get('alg', '')
        payload = jwt.decode(token, key=self.public_key, algorithms=[algorithm, ])
        return payload

