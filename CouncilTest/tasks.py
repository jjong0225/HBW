import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CouncilTest.settings')
 
app = Celery('CouncilTest')
 
# namespace='CELERY'는 모든 셀러리 관련 구성 키를 의미한다. 반드시 CELERY라는 접두사로 시작해야 한다. 
app.config_from_object('django.conf:settings', namespace='CELERY')
 
# 장고 app config에 등록된 모든 taks 모듈을 불러온다. 
app.autodiscover_tasks()
 
@app.task
def add(x, y):
    print("done")