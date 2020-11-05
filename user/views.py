import bcrypt, jwt, re, json

from django.views import View
from django.http  import JsonResponse

from .models        import User
from local_settings import SECRET_KEY, ALGORITHM
from utils          import (
    account_validate,
    password_validate
)

class SignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if account_validate(data.get('account')):
                return JsonResponse({'MESSAGE' : 'InvalidAccount'}, status = 400)

            elif password_validate(data.get('password')):
                return JsonResponse({'MESSAGE' : 'InvalidPassword'}, status = 400)

            elif User.objects.filter(account = data.get('account')):
                return JsonResponse({'MESSAGE' : 'AlreadyExistAccount'}, status = 400)

        except Exception as e:
            return JsonResponse({e}, status = 400)

        else:
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User(
                    account  = data['account'],
                    password = password.decode('utf-8')
            )
            user.full_clean()
            user.save()
            return JsonResponse({"MESSAGE": "Success"}, status = 200)

class SignIn(View):
    def post(self, request): 
        try:  
            data = json.loads(request.body)
            if password_validate(data.get('password')):
                return JsonResponse({'MESSAGE': 'InvalidPassword'}, status = 400)

            if User.objects.filter(account = data.get('account')).exists():
                user = User.objects.get(account = data.get('account'))
                if bcrypt.checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'user_id': user.id}, SECRET_KEY['secret'], ALGORITHM['algorithm']).decode('utf-8')
                    return JsonResponse({'AccessToken': access_token}, status = 200)
                return JsonResponse({'MESSAGE': 'InvalidUser'}, status = 401)
            return JsonResponse({'MESSAGE': 'InvalidUser'}, status = 401)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KeyError'}, status = 400)