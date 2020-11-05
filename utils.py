import jwt, re

from django.views import View
from django.http  import JsonResponse

from user.models    import User
from local_settings import SECRET_KEY, ALGORITHM

def account_validate(value):
    regex = re.compile(r'^[a-zA-Z0-9]{6,20}$')
    if not regex.match(value):
        return True

def password_validate(value):
    regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,20}')
    if not regex.match(value):
        return True

def login_confirm(original_function):
    def wrapper(self, request):
        try:
            access_token = request.headers.get("Authorization", None)
            if access_token:
                token_paylod    = jwt.decode(access_token, SECRET_KEY['secret'], ALGORITHM['algorithm'])
                request.account = User.objects.get(id = token_paylod['user_id'])
                return original_function(self, request)
            return JsonResponse({'MESSAGE':'Login Required'}, status = 401)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':'DecodeError'}, status = 401)

    return wrapper