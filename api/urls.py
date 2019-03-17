from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from api.views import StudentViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'unbrellas', views.UnbrellaViewSet)
router.register(r'batteries', views.BatteryViewSet)
router.register(r'lans', views.LanViewSet)
router.register(r'studytables', views.StudyTableViewSet)
router.register(r'complains', views.ComplainViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]

