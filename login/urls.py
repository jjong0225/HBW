from django.urls import path
from login import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from login.forms import custom_login_form
from django.views.static import serve
from . import models

app_name = 'login'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html', form_class=custom_login_form), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.Main, name='main'),
    path('mypage/', views.MyPage, name='mypage'),
    path('reservation/', views.StudyTableClass.LendTable, name='seltable'),
    path('reservation/submit', views.StudyTableClass.TableSelect, name='lendtable'),
    path('password_change/', views.PasswordChangeView.as_view(template_name='login/change_pw.html'), name='change'),
    path('first_login/', views.first_login_class.as_view(template_name='login/login_agreement.html'), name='first'),
    path('password_complete', views.PasswordChangeDoneView.as_view(), name='change_done'),
    path('pc/', views.PasswordChangeView.as_view(template_name='login/pass_change.html'), name='ch'),
    path('jong/', views.GetComplain, name='jong'),
    path('lendun/', views.LendUn, name='jong'),
    path('ca/', views.create_all_password),
    path('complain/', views.GetComplain),
    path('jong1/',views.EveryHourStudyTable),
    path('jong2/',views.EveryDayStudyTable),
    path('password_reset/',views.password_reset,name='password_reset'),
    path('pass_changed', views.pass_changed, name='pass_changed'),
    path('expired', views.ExpiredCheck),
    path('manage/rental/', views.ManageLentalView.as_view(), name='manage_rental'),
    path('manage/rental/<str:model>/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
