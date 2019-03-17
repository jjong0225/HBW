from .serializers import StudentSerializer, UserSerializer
from rest_framework import viewsets, filters
from login import models
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

# Create your views here.


class StudentViewSet(viewsets.ModelViewSet):
    '''
    Student에 대한 정보
    '''
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    
  


class UnbrellaViewSet(viewsets.ModelViewSet):
    '''
    우산 대여사업
    '''
    queryset = models.Unbrella.objects.all()
    serializer_class = serializers.UnbrellaSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')


class BatteryViewSet(viewsets.ModelViewSet):
    '''
    배터리 대여사업
    '''
    queryset = models.Battery.objects.all()
    serializer_class = serializers.BatterySerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')


class LanViewSet(viewsets.ModelViewSet):
    '''
    랜선 대여사업
    '''
    queryset = models.Lan.objects.all()
    serializer_class = serializers.LanSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')

class ComplainViewSet(viewsets.ModelViewSet):
    '''
    건의사항
    '''
    queryset = models.Complain.objects.all()
    serializer_class = serializers.ComplainSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number',)

class StudyTableViewSet(viewsets.ModelViewSet):
    queryset = models.StudyTable.objects.all()
    serializer_class = serializers.StudyTableSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)



class CableViewSet(viewsets.ModelViewSet):
    '''
    케이블 대여사업
    '''
    queryset = models.Cable.objects.all()
    serializer_class = serializers.CableSerializer
    permission_classes = (CustomIsAdmin, permissions.IsAdminUser)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=number', '=borrowed_by__user__username')
