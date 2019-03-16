from django.urls import path
from login import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'login'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.Main, name='main'),
    path('mypage/', views.MyPage, name='mypage'),
    path('lendunbrella/', views.LendBusinessClass.LendUnbrella, name='lendunbrella'),
    path('lendbattery/', views.LendBusinessClass.LendBattery, name='lendbattery'),
    path('lendlan/', views.LendBusinessClass.LendLan, name='lendlan'),
    path('reservation/', views.StudyTableClass.TableSelect, name='seltable'),
    path('sel/', views.StudyTableClass.LendTable, name='lendtable'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='login/login-assignment.html'), name='change'),
    path('pc/', views.PasswordChangeView.as_view(template_name='login/pass_change.html'), name='ch'),
    path('jong/', views.GetComplain, name='jong'),
    path('lendun/', views.LendUn, name='jong'),

]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
