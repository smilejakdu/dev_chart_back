import json
import jwt
import re
import bcrypt
import requests
import numpy as np

from dev_chart_back.my_settings import SECRET_KEY, ALGORITHM
from django.views               import View
from django.http                import HttpResponse, JsonResponse
from django.db.models           import Count, Q , Sum
from django.core.validators     import validate_email
from django.core.exceptions     import ValidationError
from .models                    import User

from datetime                   import datetime
from users.utils                import login_check
from pprint                     import pprint as pp



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
            'nickname'   : user.nickname,
            'date'       : f'{user.created_at.year}-{user.created_at.month}',
            'python'     : user.python,
            'javascript' : user.javascript,
            'java'       : user.java,
            'c'          : user.c,
            'c_plus'     : user.c_plus,
            'spring'     : user.spring,
            'django'     : user.django,
            'flask'      : user.flask,
            'express'    : user.express,
            'react'      : user.react,
            'vue'        : user.vue,
            'laravel'    : user.laravel,
        }for user in user_data]

        return JsonResponse({"data" : list(user_list)}, status = 200)

class ProgrammingView(View):
    @login_check
    def post(self , request):
        data = json.loads(request.body)

        try :
            user = User.objects.get(email = request.user.email)

            user.python     = data['python']
            user.javascript = data['javascript']
            user.java       = data['java']
            user.php        = data['php']
            user.c          = data['c']
            user.c_plus     = data['c_plus']
            user.spring     = data['spring']
            user.django     = data['django']
            user.flask      = data['flask']
            user.express    = data['express']
            user.react      = data['react']
            user.vue        = data['vue']
            user.laravel    = data['laravel']
            user.save()

            return HttpResponse(status = 200)

        except Exception as e :
            return JsonResponse({"message" : e} , status = 400)

    @login_check
    def get(self, request):
        user_data = User.objects.filter(email = request.user.email)

        try:

            user_list = [{
                'python'     : user.python,
                'javascript' : user.javascript,
                'java'       : user.java,
                'php'        : user.php,
                'c'          : user.c,
                'c_plus'     : user.c_plus,
                'spring'     : user.spring,
                'django'     : user.django,
                'flask'      : user.flask,
                'express'    : user.express,
                'react'      : user.react,
                'vue'        : user.vue,
                'laravel'    : user.laravel,
            }for user in user_data]

            return JsonResponse({"data" : user_list}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"} , status = 400)

        except Exception as e:
            return JsonResponse({"message":e} , status = 400)

def line_get_week_of_month(year, month, day):

    result = datetime.date(year, month, day).strftime("%V")
    if year == 2020:
        return int(result) % 40+1
    elif year == 2021:
        return int(result) + 14

class ChartDataView(View):
    def get(self, request):
        # user_data 중에 python , javascript , java ,php 에서 

        try:

            user        = User.objects.all()
            python_user = round(user.filter(python='True').count() / user.count() , 2 )

            user_list = [{
                'user_count'        : user.count(),
                'python_user_count' : python_user,
                'python'            : user.filter(python     = 'True').count(),
                'javascript'        : user.filter(javascript = 'True').count(),
                'java'              : user.filter(java       = 'True').count(),
                'php'               : user.filter(php        = 'True').count(),
                'c'                 : user.filter(c          = 'True').count(),
                'c_plus'            : user.filter(c_plus     = 'True').count(),
                'spring'            : user.filter(spring     = 'True').count(),
                'django'            : user.filter(django     = 'True').count(),
                'flask'             : user.filter(flask      = 'True').count(),
                'express'           : user.filter(express    = 'True').count(),
                'react'             : user.filter(react      = 'True').count(),
                'vue'               : user.filter(vue        = 'True').count(),
                'laravel'           : user.filter(laravel    = 'True').count(),
            }]

            return JsonResponse({"data" : user_list} , status = 200)

        except Exception as e:
            return JsonResponse({"message" :e }, status = 400)

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
