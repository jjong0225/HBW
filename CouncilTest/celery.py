from __future__ import absolute_import
from django.conf import settings
import os
 
from celery import Celery
from celery.schedules import crontab
 
# Django의 세팅 모듈을 Celery의 기본으로 사용하도록 등록합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CouncilTest.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
 
app = Celery('CouncilTest')
 
 
# 문자열로 등록한 이유는 Celery Worker가 자식 프로세스에게 configuration object를 직렬화하지 않아도 된다는것 때문
# namespace = 'CELERY'는 모든 celery 관련한 configuration key가 'CELERY_' 로 시작해야함을 의미함
app.config_from_object('django.conf:settings', namespace='CELERY')
 
# task 모듈을 모든 등록된 Django App configs에서 load 함
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'empty-month_A4-every-month-contrab': {
j           'schedule': 360.0,
    },
    'unbrella_expired_check_every_min' : {
        'task' : 'expired_check',
        'schedule' : 60.0
    },
    'reset_today_a4_every_day' : {
        'task' : 'a4_update',
        'schedule' : 360.0
    },
    'error_check_every_day' : {
        'task' : 'error_check_all',
        'schedule' : 86400.0
    },
}
