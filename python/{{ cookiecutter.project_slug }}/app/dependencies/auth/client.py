import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


class AuthClient:
    _signing_key: RSAPrivateKey | None
    _decoding_key: RSAPublicKey | None

    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key
        self._signing_key = None
        self._decoding_key = None


    @property
    def signing_key(self) -> RSAPrivateKey:
        if self._signing_key:
            return self._signing_key
        self._signing_key = serialization.load_ssh_private_key(self.private_key.encode(), password=b'')
        assert isinstance(self._signing_key, RSAPrivateKey)
        return self._signing_key

    @property
    def decoding_key(self) -> RSAPublicKey:
        if self._decoding_key:
            return self._decoding_key
        self._decoding_key = serialization.load_ssh_public_key(self.public_key.encode())
        assert isinstance(self._decoding_key, RSAPublicKey)
        return self._decoding_key

    def create_access_token(self, user_id: str) -> dict:
        token = jwt.encode(payload={'sub': user_id}, key=self.signing_key, algorithm='RS256')
        return {'access_token': token, 'token_type': 'bearer'}

    def decode_token(self, token: str) -> dict:
        header = jwt.get_unverified_header(token)
        algorithm = header.get('alg', '')
        payload = jwt.decode(token, key=self.decoding_key, algorithms=[algorithm, ])
        return payload

