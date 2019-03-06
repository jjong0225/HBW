from django.db import models
from django.contrib.auth.models import User

# Create your models here.



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

    status = models.BooleanField(default=True)
    #재학여부


    def __str__(self):
        return self.user.username
    
    objects = models.Manager()


class Unbrella(models.Model):
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
    )
    number = models.PositiveSmallIntegerField()
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length = 4, choices=status_choices, default=status_available)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        if self.status != self.status_unavailable:
            if self.borrowed_by is not None:
                self.status = self.status_borrowed
            else:
                self.status = self.status_available
        super().save(*args, **kwargs)

    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False

#실습실 테이블 모델
class StudyTable(models.Model):
    number = models.PositiveSmallIntegerField()
    is_borrowed = models.BooleanField(default = False)
    start_time = models.CharField(max_length=100, blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    lender = models.ForeignKey(Student, null=True, blank=True, on_delete=models.DO_NOTHING, db_constraint=False)

    def __str__(self):
        return "Table "+str(self.number)

    


#배터리 모델
class Battery(models.Model):
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
    )
    number = models.PositiveSmallIntegerField()
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length = 4, choices=status_choices, default=status_available)

    def __str__(self):
        return str(self.number)+"th Battery"

    def save(self, *args, **kwargs):
        if self.status != self.status_unavailable:
            if self.borrowed_by is not None:
                self.status = self.status_borrowed
            else:
                self.status = self.status_available
        super().save(*args, **kwargs)

    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False
        

#랜선 모델
class Lan(models.Model):
    status_available = '대여가능'
    status_borrowed = '대여중'
    status_unavailable = '대여불가'
    status_choices = (
        (status_available, '대여가능'),
        (status_borrowed, '대여중'),
        (status_unavailable, '대여불가'),
    )
    number = models.PositiveSmallIntegerField()
    borrowed_by = models.OneToOneField(Student, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length = 4, choices=status_choices, default=status_available)

    def __str__(self):
        return str(self.number)+"th Lan"

    def save(self, *args, **kwargs):
        if self.status != self.status_unavailable:
            if self.borrowed_by is not None:
                self.status = self.status_borrowed
            else:
                self.status = self.status_available
        super().save(*args, **kwargs)

    def is_available(self):
        if self.status == self.status_available:
            return True
        else:
            return False
        
