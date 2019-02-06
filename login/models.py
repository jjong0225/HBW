from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length = 10)
    stdID = models.CharField(max_length = 8)
    HB = models.BooleanField(default = False)
    today_A4 = models.PositiveIntegerField(default = 0)
    month_A4 = models.PositiveIntegerField(default = 0)
    battery = models.BooleanField(default = False)
    Lan = models.BooleanField(default = False)
    unbrella_borrowed = models.BooleanField(default = False)
    table_borrowed = models.BooleanField(default = False)
    StartTime = models.TimeField(blank=True, null=True)
    EndTime = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    objects = models.Manager()


class Unbrella(models.Model):
    number = models.PositiveSmallIntegerField()
    borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(UserInfo, related_name = "unbrella", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class StudyTable(models.Model):
    number = models.PositiveSmallIntegerField()
    borrowed = models.BooleanField(default = False)
    borrowed_by = models.OneToOneField(UserInfo, related_name = "table", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Table "+str(self.number)
        



