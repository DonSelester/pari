from django.contrib import admin
from django.urls import path, re_path
from bet.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index, name="index"),
    path('balance/', user_balance, name="user_balance"),
    re_path(r'^match_bet/(?P<m_id>[0-9]+)/$', match_bet, name='match_bet'),

    re_path(r'^user_payin/(?P<type>[a-zA-Z0-9_]+)/$', user_payin, name='user_payin'),
    re_path(r'^user_payout/(?P<type>[a-zA-Z0-9_]+)/$', user_payout, name='user_payout'),

    path('register/', register, name="register"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
]
