
from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from login.models import Student
from CouncilTest.celery import app
 
 

@task(name="empty_A4")
def empty():
    qs = Student.objects.all()
    for std in qs:
        std.month_A4 = 0
        std.save()
