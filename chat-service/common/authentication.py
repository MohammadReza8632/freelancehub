from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class MicroserviceJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        email = validated_token.get('email')
        role = validated_token.get('role')

        if user_id is None:
            raise InvalidToken('Token missing user_id')
        return TokenUser(user_id = user_id, email = email, role = role)


class TokenUser:
    def __init__(self, user_id, email, role):
        self.id = user_id
        self.email = email
        self.role = role
        self.is_authenticated = True

