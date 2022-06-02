from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name="home"),
    path('signup/', signup, name='signup'),  # 회원가입 페이지
    path('', login, name='login'),  # 로그인 페이지
    path('logout/', logout, name='logout'),  # 로그아웃
    path('search/', search, name='search'), # 검색
]