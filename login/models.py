from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# 대여 (학생회 측)
# 예약 (학생 측)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_data', null=True, blank=True)
    # 장고의 User모델에서 username(학번 즉 ID), password first_name, last_name, user_permissions, last_login을 사용
    # user 모델의 필드들
        # username
        # first_name
        # last_name
        # email (Optional)
        # password (Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password.) Raw passwords can be arbitrarily long and can contain any character. See the password documentation.)
        # groups
        # user_permissions
        # is_staff (Boolean)
        # is_active (Boolean)
        # is_superuser (Boolean)
        # last_login (A datetime)
        # date_joined (A datetime)

    std_year = models.CharField(max_length = 8) 
    # 17, 18 등 입학 년도 저장

    is_paid = models.BooleanField(default = False)
    # 회비 납부 여부

    today_A4 = models.PositiveIntegerField(default = 0)
    # 오늘 수령한 A4 매수

    month_A4 = models.PositiveIntegerField(default = 0)

    # 이번달 수령한 A4 매수

    #battery = models.BooleanField(default = False)
    # 배터리 대여 여부

    #lan = models.BooleanField(default = False)
    # 랜선 대여 여부

    def __str__(self):
        return self.user.username
    
    objects = models.Manager()


class Unbrella(models.Model):
    number = models.PositiveSmallIntegerField()
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.CASCADE)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.number)


#배터리 모델
class Battery(models.Model):
    number = models.PositiveSmallIntegerField()
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.DO_NOTHING)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.number)+"th Battery"
        

#랜선 모델
class Lan(models.Model):
    number = models.PositiveSmallIntegerField()
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.DO_NOTHING)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.number)+"th Lan"


class Poster(models.Model):  
    title = models.CharField(max_length=100)
    photo = models.ImageField(blank=True)
    number = models.PositiveSmallIntegerField()


#실습실 테이블 모델
class StudyTable(models.Model):
    number = models.PositiveSmallIntegerField()
    is_borrowed = models.BooleanField(default = False)
    start_time = models.CharField(max_length=100, blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    lender = models.ForeignKey(Student, null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)

    def __str__(self):
        return "Table "+str(self.number)


class timetest(models.Model):
    timea = models.DateTimeField(auto_now_add=True)
    timeb = models.DateTimeField(auto_now_add=True)
    diff = models.FloatField()


#케이블 모델, 오로지 하나의 케이블을 식별하기 위해선 number, cable_type이 필요하다 (차라리 타입말고, 번호로만 타입을 식별해본다?)
class Cable(models.Model):
    number = models.PositiveSmallIntegerField()
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.DO_NOTHING)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    cable_type = models.PositiveSmallIntegerField() # 0 : 5핀 케이블, 1 : 8핀 케이블, 2 : C타입 케이블


