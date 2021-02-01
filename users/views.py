import json
import jwt
import re
import bcrypt
import requests

from .models                    import User
from django.views               import View
from django.http                import HttpResponse, JsonResponse
from django.db.models           import Count, Q , Sum
from django.core.validators     import validate_email
from django.core.exceptions     import ValidationError
from dev_chart_back.my_settings import SECRET_KEY, ALGORITHM
from datetime                   import datetime


class SignUpView(View):
    def post(self , request):
        data = json.loads(request.body)

        try:
            for d in data:
                if not data[d]:
                    return JsonResponse({"message":f"doesnot_{d}"} , status = 400)

            validate_email(data['email'])

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "EXISTS_EMAIL"} , status = 400)

            if User.objects.filter(nickname = data['nickname']).exists():
                return JsonResponse({"message" : "EXISTS_USERNAME"} , status = 400)

            if data['password'] != data['repassword']:
                return JsonResponse({"message" : "password_check"} , status = 400)

            User(
                email    = data['email'],
                nickname = data['nickname'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ).save()

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"},status = 400)

        except Exception as e:
            return JsonResponse({"message" : e},status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_email(data['email'])

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),
                                  user.password.encode('utf-8')):

                    token = jwt.encode({'email': data['email']},
                                           SECRET_KEY['secret'],
                                           algorithm=ALGORITHM).decode('utf-8')

                    return JsonResponse({'access'   : token,
                                         'nickname' : user.nickname
                                        }, status=200, content_type="application/json")

                return HttpResponse(status=401)

            return HttpResponse(status=400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"} , status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)

        except Exception as e:
            return JsonResponse({"message" : e} , status = 400)

class UserListView(View):

    def get(self , request):

        user_data = (User.
                     objects.
                     all())

        user_list = [{
            'nickname' : user.nickname,
            'date'     : f'{user.created_at.year}-{user.created_at.month}',
        }for user in user_data]

        return JsonResponse({"data" : list(user_list)}, status = 200)

#class UserListView(View):
#
#    def get(self , request):
#        sort_by   = request.GET.get('sort_by', 'id')
#        offset    = int(request.GET.get('offset', 0))
#        limit     = int(request.GET.get('limit', 5))
#
#        user_data = (User.
#                     objects.
#                     order_by(sort_by).
#                     all()[offset:offset + limit])
#
#        user_list = [{
#            'nickname' : user.nickname,
#            'date'     : f'{user.created_at.year}-{user.created_at.month}',
#        }for user in user_data]
#
#        return JsonResponse({"data" : list(user_list)}, status = 200)
