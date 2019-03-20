from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator
from rest_framework.exceptions import APIException
from django.db import IntegrityError

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

    A4_count = models.PositiveIntegerField(default = 0, validators=[MaxValueValidator(50)], error_messages={'max_value' : '하루 대여량은 50장을 넘길 수 없습니다.'})
    # 현재 빌리려 하는 A4 매수

    today_A4 = models.PositiveIntegerField(default = 0,  validators=[MaxValueValidator(50)], error_messages={'max_value' : '하루 대여량은 50장을 넘길 수 없습니다.'})
    # 오늘 수령한 A4 매수

    month_A4 = models.PositiveIntegerField(default = 0,  validators=[MaxValueValidator(500)], error_messages={'max_value' : '한달 대여량은 500장을 넘길 수 없습니다.'})
    # 이번달 수령한 A4 매수

    is_attend = models.BooleanField(default = True)
    #재학여부

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        self.today_A4 = self.today_A4 + self.A4_count
        if self.today_A4 > 50:
            raise APIException("하루 대여량은 50장을 넘길 수 없습니다!")
        self.month_A4 = self.month_A4 + self.A4_count
        if self.month_A4 > 500:
            raise APIException("한달 대여량은 500장을 넘길 수 없습니다!")

        self.A4_count = 0
        super().save(*args, **kwargs)

    objects = models.Manager()


class Unbrella(models.Model):
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_reserved = '대여신청중'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
        (status_reserved, '대여신청중'),
    )

    number = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, null=True, related_name = "un", blank=True, on_delete=models.CASCADE)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=5, choices=status_choices, default=status_available)

    def save(self, *args, **kwargs):
        if self.is_reserved :
            self.status = self.status_reserved
        else :
            if self.status != self.status_unavailable:
                if self.borrowed_by is not None:
                    self.status = self.status_borrowed
                    self.is_borrowed = True
                    self.borrowed_time = timezone.localtime()
                else :
                    self.status = self.status_available
                    self.is_borrowed = False
        try :
            super().save(*args, **kwargs)
        except IntegrityError:
            self.borrowed_by = None
            raise APIException("같은 종류의 대여사업을 2개 이상 사용하실 수 없습니다!")
         
    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False

    def __str__(self):
        return str(self.number)


#배터리 모델
class Battery(models.Model):
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_reserved = '대여신청중'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
        (status_reserved, '대여신청중'),
    )

    number = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student,related_name='ba', null=True, blank=True, on_delete=models.DO_NOTHING)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=5, choices=status_choices, default=status_available)

    def save(self, *args, **kwargs):
        if self.is_reserved :
            self.status = self.status_reserved
        else :
            if self.status != self.status_unavailable:
                if self.borrowed_by is not None:
                    self.status = self.status_borrowed
                    self.is_borrowed = True
                    self.borrowed_time = timezone.localtime()
                else :
                    self.status = self.status_available
                    self.is_borrowed = False
        try :
            super().save(*args, **kwargs)
        except IntegrityError:
            self.borrowed_by = None
            raise APIException("같은 종류의 대여사업을 2개 이상 사용하실 수 없습니다!")
            
    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False

    def __str__(self):
        return str(self.number)+"th Battery"
        

#랜선 모델
class Lan(models.Model):
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_reserved = '대여신청중'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
        (status_reserved, '대여신청중'),
    )

    number = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, related_name='la', null=True, blank=True, on_delete=models.DO_NOTHING)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=5, choices=status_choices, default=status_available)

    def save(self, *args, **kwargs):
        if self.is_reserved :
            self.status = self.status_reserved
        else :
            if self.status != self.status_unavailable:
                if self.borrowed_by is not None:
                    self.status = self.status_borrowed
                    self.is_borrowed = True
                    self.borrowed_time = timezone.localtime()
                else :
                    self.status = self.status_available
                    self.is_borrowed = False
        try :
            super().save(*args, **kwargs)
        except IntegrityError:
            self.borrowed_by = None
            raise APIException("같은 종류의 대여사업을 2개 이상 사용하실 수 없습니다!")

    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False

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
    lender = models.ForeignKey(Student, related_name='st', null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)
    
    def __str__(self):
        return "Table "+str(self.number)




class timetest(models.Model):
    timea = models.DateTimeField(auto_now_add=True)
    timeb = models.DateTimeField(auto_now_add=True)
    diff = models.FloatField()


#케이블 모델, 오로지 하나의 케이블을 식별하기 위해선 number, cable_type이 필요하다 (차라리 타입말고, 번호로만 타입을 식별해본다?)
class Cable(models.Model):
    type_c = 'C타입 케이블'
    type_5= '5핀 케이블'
    type_8 = '8핀 케이블'
    type_choices = (
        (type_c, 'C타입 케이블'),
        (type_5, '5핀 케이블'),
        (type_8, '8핀 케이블'),
    )
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_reserved = '대여신청중'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
        (status_reserved, '대여신청중'),
    )
    
    number = models.PositiveSmallIntegerField(primary_key=True, unique=True)
    is_borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(Student, related_name='ca', null=True, blank=True, on_delete=models.DO_NOTHING)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    is_reserved = models.BooleanField(default = False)
    reservation_time = models.DateTimeField(auto_now_add=True)
    cable_type = models.CharField(max_length=10, choices=type_choices, default=type_5)
    status=models.CharField(max_length=5, choices=status_choices, default=status_available)

    def __str__(self):
        return (str(self.number))+"th cable"

    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if self.is_reserved :
            self.status = self.status_reserved
        else :
            if self.status != self.status_unavailable:
                if self.borrowed_by is not None:
                    self.status = self.status_borrowed
                    self.is_borrowed = True
                    self.borrowed_time = timezone.localtime()
                else :
                    self.status = self.status_available
                    self.is_borrowed = False
        try :
            super().save(*args, **kwargs)
        except IntegrityError:
            self.borrowed_by = None
            raise APIException("같은 종류의 대여사업을 2개 이상 사용하실 수 없습니다!")

class Complain(models.Model):
    number = models.CharField(max_length=1000)
    updated_text = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default = True)
    username = models.CharField(max_length = 10)
    userid = models.CharField(max_length = 8)

class time_table(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.PositiveSmallIntegerField(default = 0)

class now_time_table(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.PositiveSmallIntegerField(default = 0)
    is_manager = models.BooleanField(default = False)