from django.urls import path
from .views      import (SignUpView ,
                         SignInView)

urlpatterns = [
    path("/login"    , SignInView.as_view()),
    path("/register" , SignInView.as_view()),
]
