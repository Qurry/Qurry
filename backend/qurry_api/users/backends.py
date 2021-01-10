import jwt

from django.core.exceptions import PermissionDenied, RequestAborted
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from .models import User

class JWTAuthentication(ModelBackend):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.validate(raw_token)
        return self.get_user(validated_token)

    def get_user(self, validated_token):
        
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise jwt.InvalidTokenError('Token contained no recognizable user identification')

        user = User.objects.get(id=user_id)

        if not user.is_active:
            raise PermissionDenied('User is inactive')
        
        return user
    
    def get_header(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')

        if isinstance(header, str):
            header = header.encode('iso-8859-1')

        return header
    
    def get_raw_token(self, header):
        parts = header.split()

        if len(parts) == 0:
            return None

        if parts[0] not in list(h.encode('iso-8859-1') for h in ['Bearer',]):
            return None

        if len(parts) != 2:
            raise RequestAborted('Authorization header must contain two space-delimited values')

        return parts[1]

    def validate(self, raw_token):
        # TODO
        # validate token after outstanding tokens and blacklist
        return jwt.decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])

