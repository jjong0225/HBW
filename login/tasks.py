from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from login.models import Student
from django.conf import settings
from CouncilTest.celery import app
from django.utils import timezone
from login import models
import datetime
import logging
logger = logging.getLogger(__name__)
 
 

# 매 분마다 호출되는 task, 필요 시 모든 복지사업으로 확장 (우선 우산만)
@task(name="expired_check")
def ExpiredCheck():
    unbrella_set = models.Unbrella.objects.all().filter(is_reserved = True).filter(is_borrowed = False)
    cur_time = timezone.now()
    for item in unbrella_set :
        if item.reservation_time+datetime.timedelta(minutes=10) < cur_time :
            item.is_reserved = False
            item.borrowed_by = None
            item.save()


@task(name="a4_update")
def EveryDayStudentReset():
    student_q = models.Student.objects.all().update(today_A4 = 0)


@task(name="empty_A4")
def empty():
    models.Student.objects.all().update(month_A4=0)
    

# 매일 쿼리셋의 오류체크 
@task(name="error_check_all")
def EveryDayErrorCheck ():
    unbrella_q = models.Unbrella.objects.all()
    battery_q = models.Battery.objects.all()
    lan_q = models.Lan.objects.all()
    studytable_q = models.StudyTable.objects.all()

    unbrella_count = 12
    battery_count = 10
    lan_count = 5
    studytable_day_count = 1
    studytable_table_count = 10
    studytable_time_count = 8
    studytable_count = studytable_day_count * studytable_table_count * studytable_time_count

    
    # 우산 예약 레코드
    if unbrella_count != unbrella_q.count() :
        unbrella_arr= [0 for _ in range(unbrella_count + 1)]
        i = 1
        while i <= unbrella_count :
            unbrella_arr[i] = models.Unbrella.objects.all().filter(number=i).count()
            i = i + 1
        i = 1
        while i <= unbrella_count :
            if  unbrella_arr[i] > 1 :
                p = models.Unbrella.objects.filter(number=i).filter(is_borrowed=False).filter(is_reserved=False).delete()
                unbrella_arr[i] = models.Unbrella.objects.all().filter(number=i).count()

            if unbrella_arr[i] == 0 :
                p = models.Unbrella.objects.create(number = i, is_borrowed = False, borrowed_by = None, 
                borrowed_time = timezone.localtime(), is_reserved = False, reservation_time = timezone.localtime() )
            i = i + 1
    if(unbrella_q.count() != unbrella_count):
        print("Server Error : 중복된 우산 레코드가 존재합니다. Admin 사이트에서 이를 직접 관리하거나 서버 관리자에게 문의해주세요")

    # 배터리 예약 레코드
    if battery_count != battery_q.count() :
        battery_arr= [0 for _ in range(battery_count + 1)]
        i = 1
        while i <= battery_count :
            battery_arr[i] = models.Battery.objects.all().filter(number=i).count()
            i = i + 1
        i = 1
        while i <= battery_count :
            if  battery_arr[i] > 1 :
                p = models.Battery.objects.filter(number=i).filter(is_borrowed=False).filter(is_reserved=False).delete()
                battery_arr[i] = models.Battery.objects.all().filter(number=i).count()

            if battery_arr[i] == 0 :
                p = models.Battery.objects.create(number = i, is_borrowed = False, borrowed_by = None, 
                borrowed_time = timezone.localtime(), is_reserved = False, reservation_time = timezone.localtime() )
            i = i + 1

    if(battery_q.count() != battery_count):
        print("Server Error : 중복된 배터리 레코드가 존재합니다. Admin 사이트에서 이를 직접 관리하거나 서버 관리자에게 문의해주세요")


    # 랜선 예약 레코드
    if lan_count != lan_q.count() :
        lan_arr= [0 for _ in range(lan_count + 1)]
        i = 1
        while i <= lan_count :
            lan_arr[i] = models.Lan.objects.all().filter(number=i).count()
            i = i + 1
        i = 1
        while i <= lan_count :
            if  lan_arr[i] > 1 :
                p = models.Lan.objects.filter(number=i).filter(is_borrowed=False).filter(is_reserved=False).delete()
                lan_arr[i] = models.Lan.objects.all().filter(number=i).count()

            if lan_arr[i] == 0 :
                p = models.Lan.objects.create(number = i, is_borrowed = False, borrowed_by = None, 
                borrowed_time = timezone.localtime(), is_reserved = False, reservation_time = timezone.localtime() )
            i = i + 1

    if(lan_q.count() != lan_count):
        print("Server Error : 중복된 랜 레코드가 존재합니다. Admin 사이트에서 이를 직접 관리하거나 서버 관리자에게 문의해주세요")



    # 실습실 예약 레코드, 우선 하루에 대한 레코드들만 존재하므로, Number, start_time로 유일한 레코드들을 식별 가능하다
    if studytable_count != studytable_q.count() :
        Number = 1
        off_set = 9 # 예약을 받는 최초 시간 - 1의 값으로 줘야 한다
        while Number <= studytable_table_count :
            now_q = studytable_q.filter(number=Number)
            studytable_arr= [0 for _ in range(studytable_time_count + 1)]
            i = 1
            while i <= studytable_time_count :
                studytable_arr[i] = now_q.filter(start_time = i + off_set).count()
                i = i + 1
            i = 1
            while i <= studytable_time_count :
                if  studytable_arr[i] > 1 :
                    now_q.filter(start_time = i + off_set).filter(is_borrowed=False).delete()
                    studytable_arr[i] = now_q.filter(start_time=i + off_set).count()

                if studytable_arr[i] == 0 :
                    models.StudyTable.objects.create(number = Number, is_borrowed = False,  start_time = i + off_set, lender = None)
                i = i + 1
            Number = Number + 1


    if(studytable_q.count() != studytable_table_count):
        print("Server Error : 중복된 실습실 레코드가 존재합니다. Admin 사이트에서 이를 직접 관리하거나 서버 관리자에게 문의해주세요")



@task(name="logging_admin")
def LoggingAdminTask() :
    logs = LogEntry.objects.all()
    for log in logs :
        action_time = models.DateTimeField(_('action time'), auto_now=True)
        user = models.ForeignKey(settings.AUTH_USER_MODEL)
        content_type = models.ForeignKey(ContentType, blank=True, null=True)
        object_id = models.TextField(_('object id'), blank=True, null=True)
        object_repr = models.CharField(_('object repr'), max_length=200)
        action_flag = models.PositiveSmallIntegerField(_('action flag'))
        change_message = models.TextField(_('change message'), blank=True)
        logger.info('우산 사업 : [학번:'+request.user.username+'|우산 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}


def GetNowManager() :
    models.now_time_table.objects.all().delete()
    current_time = timezone.localtime()

    num = (current_time.hour - 9) * 2
    if current_time.minute > 30 :
        num = num + 1

    now_manager = models.time_table.objects.all().filter(start_time = num)
    if now_manager.count() == 0 :
        models.now_time_table.objects.create(name='blank', start_time = num, is_staff = False)    
    else if  now_manager.count() == 1 :
        models.now_time_table.objects.create(name=now_manager.name, start_time = num, is_manage = True)
    else  ## 오류 상황
        models.now_time_table.objects.create(name='blank', start_time = num, is_staff = False)    
    