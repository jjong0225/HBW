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
    'reset_month_a4_every_month': {
        'task' : 'empty_A4',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'),
    },
    'item_expired_check_every_min' : {
        'task' : 'expired_check',
        'schedule' : crontab(),
    },
    'reset_today_a4_every_day' : {
        'task' : 'a4_update',
        'schedule' : crontab(minute=0, hour=0),
    },
    'time_table_check_every_30_minutes' : {
        'task': 'get_now_manager',
        'schedule': crontab(minute='20, 50'),
    },
    'study_table_day_update': {
        'task': 'table_day_update',
        'schedule': crontab(minute=0, hour=0),
    },
    'study_table_hour_update': {
        'task': 'table_hour_update',
        'schedule': crontab(minute=0),
    },
}
