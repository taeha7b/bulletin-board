import json

from django.views import View
from django.http  import JsonResponse

from .models import Posting
from utils   import login_confirm


class Board(View):
    @login_confirm
    def post(self, request):
        try:
            data = json.loads(request.body)
            Posting.objects.create(
                user    = request.account,
                content = data.get('content')
            )
            return JsonResponse({'MESSAGE': 'Success'}, status = 200)
        
        except Exception:
            return JsonResponse({'MESSAGE': 'Unsuccess'},status = 400)

    def get(self, request):
        try:
            posting = list(Posting.objects.filter(is_deleted = False).values())
            return JsonResponse({'MESSAGE': posting}, status = 200)

        except Exception:
            return JsonResponse({'MESSAGE': 'Unsuccess'},status = 400)

    @login_confirm
    def put(self , request):
        try:
            data       = json.loads(request.body)
            user_id    = request.account.id
            posting_id = data['posting_id']
            content    = data['content']
            revised_posting = Posting.objects.get(
                id   = posting_id,
                user = user_id
            )
            
            revised_posting.content = content
            revised_posting.save()
            return JsonResponse({'MESSAGE': 'Success'}, status = 200)
        
        except Exception:
            return JsonResponse({'MESSAGE': 'Unsuccess'}, status = 400)

    @login_confirm
    def delete(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.account.id
            posting_id = data['posting_id']
            revised_posting = Posting.objects.get(
                id   = posting_id,
                user = user_id
            )
            
            revised_posting.is_deleted = True
            revised_posting.save()
            return JsonResponse({'MESSAGE': 'Success'}, status = 200)
        
        except Exception:
            return JsonResponse({'MESSAGE': 'Unsuccess'}, status = 400)

