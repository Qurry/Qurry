from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthenticatedView(View):
    def setup(self, request, *args, **kwargs):
        self.user = None
        
        # user_token = JWTAuthentication().authenticate(request)
        # it returns this: (<User: admin>, {'token_type': 'access', 'exp': 1609611652, 'jti': 'a99308ebe15f4f6d8522e770aa42c50d', 'user_id': 'afdbd33c-5f31-4672-93f1-8d1cad47bbcf'})
        
        # TODO
        # 1. check whether token is valid with: jwt.decode(encoded, "secret", algorithms=["HS256"]) !!!Important: check if Hacker removed signature!!!
        # 2. check if token is in Blocklist
        # 3. Not sure but maybe get user from database
        
        if user_token:
            self.user = user_token[0]
        return super().setup(request, *args, **kwargs)
