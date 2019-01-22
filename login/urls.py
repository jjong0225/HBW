from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('<int:pk>/edit/', views.UserEdit, name='user_edit'),
    path('<int:pk>/show/', views.UserShow, name='user_show'),
]
