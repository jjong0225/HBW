from django.urls import path
from login import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'login'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/final_login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.Main, name='main'),
    path('mypage/', views.MyPage, name='mypage'),
    path('lendunbrella/', views.LendUnbrella, name='lendunbrella'),
    path('lendbattery/', views.LendBattery, name='lendbattery'),
    path('lendlan/', views.LendLan, name='lendlan'),
    path('reservation/', views.TableSelect, name='seltable'),
    path('sel/', views.LendTable, name='lendtable'),
]
