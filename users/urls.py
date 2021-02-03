from django.urls import path
from .views      import (SignUpView ,
                         SignInView ,
                         UserListView ,
                         ProgrammingView,
                         ChartDataView)

urlpatterns = [
    path("login"       , SignInView.as_view()),
    path("register"    , SignUpView.as_view()),
    path("userlist"    , UserListView.as_view()),
    path("programming" , ProgrammingView.as_view()),
    path("chartdata"   , ChartDataView.as_view()),
]
