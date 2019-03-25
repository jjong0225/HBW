from django.urls import path
from login import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from login.forms import custom_login_form

app_name = 'login'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html', form_class=custom_login_form), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.Main, name='main'),
    path('mypage/', views.MyPage, name='mypage'),
    path('reservation/', views.StudyTableClass.LendTable, name='seltable'),
    path('reservation/submit', views.StudyTableClass.TableSelect, name='lendtable'),
    path('password_change/', views.PasswordChangeView.as_view(template_name='login/change_pw.html'), name='change'),
    path('pc/', views.PasswordChangeView.as_view(template_name='login/pass_change.html'), name='ch'),
    path('jong/', views.GetComplain, name='jong'),
    path('lendun/', views.LendUn, name='jong'),
    path('ca/', views.create_all_password),
    path('complain/', views.GetComplain),
    path('jong1/',views.EveryDayErrorCheck),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
