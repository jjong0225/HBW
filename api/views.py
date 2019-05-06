from .serializers import StudentSerializer, UserSerializer
from rest_framework import viewsets, filters
from login import models
from api.models import Logging
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from api import serializers
from api.permissions import CustomIsAdmin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.db import IntegrityError
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class StudentViewSet(viewsets.ModelViewSet):
    '''
    Student에 대한 정보
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)      
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username',)
    
    #def perform_create(self, serializer):
     #   serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    '''
    User(계정)에 대한 정보
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    
  


class UnbrellaViewSet(viewsets.ModelViewSet):
    '''
    우산 대여사업
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.Unbrella.objects.all().order_by('number')
    serializer_class = serializers.UnbrellaSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')


class BatteryViewSet(viewsets.ModelViewSet):
    '''
    배터리 대여사업
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.Battery.objects.all().order_by('number')
    serializer_class = serializers.BatterySerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')


class LanViewSet(viewsets.ModelViewSet):
    '''
    랜선 대여사업
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.Lan.objects.all().order_by('number')
    serializer_class = serializers.LanSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')

class ComplainViewSet(viewsets.ModelViewSet):
    '''
    건의사항
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.Complain.objects.all()
    serializer_class = serializers.ComplainSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number',)

class StudyTableViewSet(viewsets.ModelViewSet):
    '''
    실습실 테이블
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.StudyTable.objects.all()
    serializer_class = serializers.StudyTableSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number',)


class CableViewSet(viewsets.ModelViewSet):
    '''
    케이블 대여사업
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = models.Cable.objects.all().order_by('number')
    serializer_class = serializers.CableSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')


class LoggingViewSet(viewsets.ModelViewSet):
    '''
    로그
    '''
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) # important
    queryset = Logging.objects.all().order_by('-pk')
    serializer_class = serializers.LoggingSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user', '=item')
    
