from django.urls import path
from .views      import (SignUpView ,
                         SignInView ,
                         UserListView)

urlpatterns = [
    path("login"    , SignInView.as_view()),
    path("register" , SignUpView.as_view()),
    path("userlist" , UserListView.as_view())
]
