#HBW/api/serializers.py

from rest_framework import serializers
from login import models
from django.contrib.auth.models import User

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset = User.objects.all(), required=False, allow_null=True)
    user_info = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Student
        fields = ('url', 'user_info', 'user', 'std_year', 'is_paid',
                'today_A4', 'month_A4')



class UserSerializer(serializers.ModelSerializer):
    user_data = StudentSerializer(read_only=True)

    class Meta:
        model = User
        fields = ( 'url', 'id', 'username', 'last_name', 'first_name', 'user_data')
        write_only_fields = ('password',)
        



class UnbrellaSerializer(serializers.ModelSerializer):
    borrowed_by = serializers.HyperlinkedRelatedField(view_name='student-detail', queryset=models.Student.objects.all(), required=False, allow_null = True)

    class Meta:
        model = models.Unbrella
        fields = ('url', 'number', 'is_borrowed', 'borrowed_by')


class BatterySerializer(serializers.ModelSerializer):
    borrowed_by = serializers.HyperlinkedRelatedField(view_name='student-detail', queryset=models.Student.objects.all(), required=False, allow_null = True)

    class Meta:
        model = models.Battery
        fields = ('url', 'number', 'is_borrowed', 'borrowed_by')


class LanSerializer(serializers.ModelSerializer):
    borrowed_by = serializers.HyperlinkedRelatedField(view_name='student-detail', queryset=models.Student.objects.all(), required=False, allow_null = True)

    class Meta:
        model = models.Lan
        fields = ('url', 'number', 'is_borrowed', 'borrowed_by')


class StudyTableSerializer(serializers.ModelSerializer):
    lender = serializers.HyperlinkedRelatedField( view_name='student-detail', queryset=models.Student.objects.all(), required=False, allow_null=True)

    class Meta:
        model = models.StudyTable
        fields = ('url', 'number', 'is_borrowed', 'start_time', 'end_time', 'lender')