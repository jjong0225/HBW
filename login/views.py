from django.shortcuts import render, get_object_or_404, redirect
from login.models import Student, StudyTable
from login import models
from login.forms import UserForm, TableForm, TimeForm, PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
import datetime
from django.db.models import Q
import logging
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
logger = logging.getLogger(__name__)


from urllib.parse import urlparse, urlunparse
from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

# Create your views here.


class UserHandlingClass () :
    # 'name', 'stdID', 'HB'
    def Signup(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                new_user = User.objects.create_user(**form.cleaned_data)
                login(request, new_user)
                return redirect('login:main')
        else:
            form = UserForm()
            return render(request, 'login/signup.html', {'form': form})

    def Signin(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('login:main')
            else:
                return HttpResponse(user)
        else:
            form = UserForm()
            return render(request, 'login/final_login.html', {'form': form})


def Main(request):
    unbrella_set = models.Unbrella.objects.all()
    battery_set = models.Battery.objects.all()
    lan_set = models.Lan.objects.all()
    cable_set = models.Cable.objects.all()
    post_q = models.Poster.objects.all().order_by('number')
    table_q = models.StudyTable.objects.all().order_by('number', 'start_time')
    manager = models.now_time_table.objects.all()
    unbrella_count = unbrella_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    battery_count = battery_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    lan_count = lan_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    cable_count = cable_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    message_unbrella = ""
    message_battery = ""
    message_lan = ""
    message_cable = ""
    unbrella_status = 0   # 0 : 평상시상태.   1 : 대여가능.   2 : 대여중   3 : 대여가능한 물품이 없음 
    battery_status = 0  
    lan_status = 0
    cable_status = 0 
    login_status = 0

    if request.method == "POST":
        if request.user.is_authenticated == False :
            login_status = 1
            return render(request, 'login/home.html', {
                'tables' : table_q,
                'battery_count': battery_count,
                'unbrella_count': unbrella_count,
                'lan_count': lan_count,
                'cable_count': cable_count,
                'posts':post_q,
                'battery_total' : battery_set.count(),
                'unbrella_total': unbrella_set.count(),
                'lan_total': lan_set.count(),
                'cable_total': cable_set.count(),
                'message_unbrella': message_unbrella,
                'message_battery': message_battery,
                'message_lan': message_lan,
                'message_cable': message_cable,
                'unbrella_status': unbrella_status,
                'battery_status': battery_status,
                'lan_status': lan_status,
                'cable_status': cable_status,   
                'manager':manager,   
                'login_status':login_status,  
            })

        if request.user.user_data.is_paid == False :
            login_status = 2
            return render(request, 'login/home.html', {
                'tables' : table_q,
                'battery_count': battery_count,
                'unbrella_count': unbrella_count,
                'lan_count': lan_count,
                'cable_count': cable_count,
                'posts':post_q,
                'battery_total' : battery_set.count(),
                'unbrella_total': unbrella_set.count(),
                'lan_total': lan_set.count(),
                'cable_total': cable_set.count(),
                'message_unbrella': message_unbrella,
                'message_battery': message_battery,
                'message_lan': message_lan,
                'message_cable': message_cable,
                'unbrella_status': unbrella_status,
                'battery_status': battery_status,
                'lan_status': lan_status,
                'cable_status': cable_status,   
                'manager':manager,   
                'login_status':login_status,  
            })

        if request.POST.get('battery', 'False') == "True":
            if battery_count == battery_set.count():
                battery_status = 3
            else :
                try :
                    if request.user.user_data.ba is not None :
                        battery_status = 2
                except :      
                    for item in battery_set:
                        if item.is_available():
                            break
                    message_battery = str(item.number)+"번 배터리가 대여되었습니다."
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('보조배터리 사업 : [학번:'+request.user.username+'|보조배터리 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                    battery_count = battery_count + 1
                    battery_status = 1

        if request.POST.get('unbrella', 'False') == "True":
            if unbrella_count == unbrella_set.count():
                unbrella_status = 3
            else :
                try :
                    if request.user.user_data.un is not None :
                        unbrella_status = 2
                except :      
                    for item in unbrella_set:
                        if item.is_available():
                            break
                    message_unbrella = str(item.number)+"번 우산이 대여되었습니다."
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('우산 사업 : [학번:'+request.user.username+'|우산 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                    unbrella_count = unbrella_count + 1
                    unbrella_status = 1

        if request.POST.get('lan', 'False') == "True":
            if lan_count == lan_set.count():
                lan_status = 3
            else :
                try :
                    if request.user.user_data.la is not None :
                        lan_status = 2
                except :      
                    for item in lan_set:
                        if item.is_available():
                            break
                    message_lan = str(item.number)+"번 랜선이 대여되었습니다."
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('랜선 사업 : [학번:'+request.user.username+'|랜선 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                    lan_count = lan_count + 1
                    lan_status = 1

        if request.POST.get('cable', 'False') == "True":
            if cable_count == cable_set.count():
                cable_status = 3
            else :
                try :
                    if request.user.user_data.ca is not None :
                        cable_status = 2
                except :      
                    for item in cable_set:
                        if item.is_available():
                            break
                    message_cable = str(item.number)+"번 케이블이 대여되었습니다."
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('케이블 사업 : [학번:'+request.user.username+'|케이블 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                    cable_count = cable_count + 1
                    cable_status = 1
            
    return render(request, 'login/home.html', {
        'tables' : table_q,
        'battery_count': battery_count,
        'unbrella_count': unbrella_count,
        'lan_count': lan_count,
        'cable_count': cable_count,
        'posts':post_q,
        'battery_total' : battery_set.count(),
        'unbrella_total': unbrella_set.count(),
        'lan_total': lan_set.count(),
        'cable_total': cable_set.count(),
        'message_unbrella': message_unbrella,
        'message_battery': message_battery,
        'message_lan': message_lan,
        'message_cable': message_cable,
        'unbrella_status': unbrella_status,
        'battery_status': battery_status,
        'lan_status': lan_status,
        'cable_status': cable_status,   
        'manager':manager,   
        'login_status':login_status,  
    })

#마이페이지
@login_required
def MyPage(request):
    if request.user.date_joined.year == 2019 and request.user.date_joined.month == 3 and request.user.date_joined.day == 28 :
        return redirect('login:first') 
    current_user = request.user
    cur_time = timezone.localtime()
    manager = models.now_time_table.objects.all()


    if request.method == "POST":
        cur_time = request.POST.get('cancel')
        time = StudyTable.objects.all().filter(lender_id=current_user.user_data.id).filter(start_time=cur_time).first()
        if time is None : 
            return HttpResponse("예약이 존재하지 않습니다.")
        if int(cur_time) > timezone.localtime().hour : 
            time.is_borrowed = False
            time.lender_id = None
            time.save()
        else :
            time.lender_id = None
            time.save()
        time_q = StudyTable.objects.all().filter(lender_id=current_user.user_data.id)
        return HttpResponse("취소 되었습니다.")
    else:
        time_q = StudyTable.objects.all().filter(lender_id=current_user.user_data.id)
        my_unbrella = models.Unbrella.objects.filter(borrowed_by = request.user.user_data).first()
        my_battery = models.Battery.objects.filter(borrowed_by = request.user.user_data).first()
        my_lan = models.Lan.objects.filter(borrowed_by = request.user.user_data).first()
        my_cable = models.Cable.objects.filter(borrowed_by = request.user.user_data).first()

        unbrella_status = 0
        battery_status = 0
        lan_status = 0
        cable_status = 0

        unbrella_time = 0
        battery_time = 0
        lan_time = 0
        cable_time = 0

        if my_unbrella is None : 
            unbrella_status = 0
        else :
            if my_unbrella.is_borrowed == True : 
                if (my_unbrella.borrowed_time + datetime.timedelta(days = 1)) > timezone.localtime() :
                    unbrella_status = 1
                    if my_unbrella.borrowed_time.weekday() < 4 :
                        tmp_time = ((my_unbrella.borrowed_time + datetime.timedelta(days = 1)) - timezone.localtime())
                        unbrella_time = tmp_time 
                    else :
                        offset = 7 - timezone.localtime().weekday()
                        tmp_time = ((my_unbrella.borrowed_time + datetime.timedelta(days = offset)) - timezone.localtime())
                        unbrella_time = tmp_time.days * 24 + (tmp_time.seconds // 3600)
                else : 
                    unbrella_status = 2
                    tmp_time =  timezone.localtime() - my_unbrella.borrowed_time
                    unbrella_time = tmp_time.days
            elif my_unbrella.is_reserved == True :
                    unbrella_status = 3
                    unbrella_time = ((((my_unbrella.reservation_time + datetime.timedelta(minutes = 10)) - timezone.localtime()).seconds) % 3600) // 60

        if my_battery is None : 
            battery_status = 0
        else :
            if my_battery.is_borrowed == True : 
                if (my_battery.borrowed_time + datetime.timedelta(days = 1)) > timezone.localtime() :
                    battery_status = 1
                    if my_battery.borrowed_time.weekday() < 4 :
                        tmp_time = ((my_battery.borrowed_time + datetime.timedelta(days = 1)) - timezone.localtime())
                        battery_time = tmp_time 
                    else :
                        offset = 7 - timezone.localtime().weekday()
                        tmp_time = ((my_battery.borrowed_time + datetime.timedelta(days = offset)) - timezone.localtime())
                        battery_time = tmp_time.days * 24 + (tmp_time.seconds // 3600)
                else : 
                    battery_status = 2
                    tmp_time =  timezone.localtime() - my_battery.borrowed_time
                    battery_time = tmp_time.days
            elif my_battery.is_reserved == True :
                    battery_status = 3
                    battery_time = ((((my_battery.reservation_time + datetime.timedelta(minutes = 10)) - timezone.localtime()).seconds) % 3600) // 60

        if my_lan is None : 
            lan_status = 0
        else :
            if my_lan.is_borrowed == True : 
                if (my_lan.borrowed_time + datetime.timedelta(days = 1)) > timezone.localtime() :
                    lan_status = 1
                    if my_lan.borrowed_time.weekday() < 4 :
                        tmp_time = ((my_lan.borrowed_time + datetime.timedelta(days = 1)) - timezone.localtime())
                        lan_time = tmp_time 
                    else :
                        offset = 7 - timezone.localtime().weekday()
                        tmp_time = ((my_lan.borrowed_time + datetime.timedelta(days = offset)) - timezone.localtime())
                        lan_time = tmp_time.days * 24 + (tmp_time.seconds // 3600)
                else : 
                    lan_status = 2
                    tmp_time =  timezone.localtime() - my_lan.borrowed_time
                    lan_time = tmp_time.days
            elif my_lan.is_reserved == True :
                    lan_status = 3
                    lan_time = ((((my_lan.reservation_time + datetime.timedelta(minutes = 10)) - timezone.localtime()).seconds) % 3600) // 60

        if my_cable is None : 
            cable_status = 0
        else :
            if my_cable.is_borrowed == True : 
                if (my_cable.borrowed_time + datetime.timedelta(days = 1)) > timezone.localtime() :
                    cable_status = 1
                    if my_cable.borrowed_time.weekday() < 4 :
                        tmp_time = ((my_cable.borrowed_time + datetime.timedelta(days = 1)) - timezone.localtime())
                        cable_time = tmp_time 
                    else :
                        offset = 7 - timezone.localtime().weekday()
                        tmp_time = ((my_cable.borrowed_time + datetime.timedelta(days = offset)) - timezone.localtime())
                        cable_time = tmp_time.days * 24 + (tmp_time.seconds // 3600)
                else : 
                    cable_status = 2
                    tmp_time =  timezone.localtime() - my_cable.borrowed_time
                    cable_time = tmp_time.days
            elif my_cable.is_reserved == True :
                    cable_status = 3
                    cable_time = ((((my_cable.reservation_time + datetime.timedelta(minutes = 10)) - timezone.localtime()).seconds) % 3600) // 60

        cur_time  = timezone.localtime()
        return render(request, 'login/mypage.html', {
            'times' : time_q,
            'cur_time' : cur_time, 
            'manager':manager,
            'my_unbrella' : my_unbrella, 
            'my_battery' : my_battery, 
            'my_lan' : my_lan, 
            'my_cable' : my_cable,
            'unbrella_time' : unbrella_time, 
            'battery_time' : battery_time, 
            'lan_time' : lan_time, 
            'cable_time' : cable_time, 
            'unbrella_status' : unbrella_status, 
            'battery_status' : battery_status, 
            'lan_status' : lan_status, 
            'cable_status' : cable_status, 
            'cur_time' : cur_time,
            })


class StudyTableClass() :
    def TableSelect(request):
        if request.method == "POST":
            sel_table = request.POST.get('tableNum')
            sel_time = [0,0,0,0]
            for i in range(0,4):
                post_name = 'time[' + str(i) + ']'
                if request.POST.get(post_name) != 0 :
                    sel_time[i] = request.POST.get(post_name)
            table_q = StudyTable.objects.all().filter(number=sel_table).filter(start_time__in=sel_time).filter(is_borrowed=False)
            if StudyTable.objects.all().filter(lender=request.user.user_data.id).count() + table_q.count() > 4 :
                return HttpResponse("초과 예약")

            for table in table_q :
                if StudyTable.objects.all().filter(lender =request.user.user_data.id).filter(start_time = table.start_time).count() > 0 :
                    print("동일 시간에 다른테이블 예약 존재")
                    return HttpResponse("동일 시간에 다른테이블 예약 존재")
                if table.is_borrowed == True :
                    print("다른 사람의 예약 존재")
                    return HttpResponse("다른 사람의 예약 존재")

            for sel in table_q:
                sel.is_borrowed = True
                sel.lender = request.user.user_data
                sel.save()
                logger.info('실습실 사업 : [학번:'+request.user.username+'| 실습실 테이블 번호:'+str(sel.number)+'| 실습실 대여 시간:'+ str(sel.start_time)+'] 예약 완료') # 담당자:{}
            return HttpResponse("예약되었습니다.")


#            if request.POST.get('desk') is not None:
#                selected_number = request.POST['desk']
#                table_q = StudyTable.objects.all().filter(number=selected_number)
#                return render(request, 'login/place_reservation.html', {'tables' : table_q})
#            else:
#                return render(request, 'login/place_reservation.html')            


    @login_required
    def LendTable(request):
        if request.user.date_joined.year == 2019 and request.user.date_joined.month == 3 and request.user.date_joined.day == 28 :
            return redirect('login:first') 
        sel_num = request.GET.get('table')
        table_q = StudyTable.objects.all().filter(number=sel_num)
        manager = models.now_time_table.objects.all()    
        return render(request, 'login/place_reservation.html', { 'tables' : table_q, 'manager':manager})
#         if request.method == "POST":
#             sel_time = request.POST.get('tableNum')
#             sel_table = request.POST.getlist('time[]')
#             table_q = StudyTable.objects.all().filter(start_time__in=sel_time).filter(number=sel_table).filter(is_borrowed=False)
#             print(table_q)
#             if StudyTable.objects.all().filter(lender =request.user.user_data.id).count()+ table_q.count() > 4 :
#                 yes_no = 1
#                 return render(request, 'login/place_reservation.html', {'yes_no' : yes_no})
#             for table in table_q :
#                 if StudyTable.objects.all().filter(lender =request.user.user_data.id).filter(start_time = table.start_time).count() > 0 :
#                     yes_no = 2
#                     return render(request, 'login/place_reservation.html', {'yes_no' : yes_no})
# #            for sel in table_q:
# #                    sel.is_borrowed = True
# #                    sel.lender = request.user.user_data
# #                    sel.save()
# #                    logger.info('실습실 사업 : [학번:'+request.user.username+'| 실습실 테이블 번호:'+str(sel.number)+'| 실습실 대여 시간:'+ str(sel.start_time)+'] 예약 완료') # 담당자:{}
# #            return redirect('login:seltable')
#         else:
#             yes_no = 0
#             return render(request, 'login/place_reservation.html', {'yes_no' : yes_no})




class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context
      
class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login:change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'login/password_change_done.html'
    title = _('Password change successful')
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# 우산의 번호를 받아 우산을 반환 (Post 방식)
# 만약 프로그램 내에서 변경이 불가하다면, 이를 이용 (나머지는 같은 방식으로 이름만 조금 바꾸자.)
def ReturnUnbrella(request):
    if request.method == "POST":
        num = request.POST['num']
        item_q = models.Unbrella.objects.all() # 오직 하나의 객체
        if int(num) <= item_q.count() and int(num) >= 0 :
            item_q = models.Unbrella.objects.all().filter(number=num) # 오직 하나의 객체
            for item in item_q :
                if item.is_borrowed == True :
                    item.is_borrowed = False
                    item.borrowed_time = timezone.localtime()
                    item.borrowed_by = None
                    item.save()
                else:
                    print("해당 우산은 대여되지 않았습니다.")
        else:
            print("올바른 우산 번호가 아닙니다.")
    return redirect('login:main')



# POST의 각 Field들인 XXX를 정의해야함 
def GetComplain(request):
    if request.method == "POST":
        anonymous_check  = request.POST['is_anonymous']
        updater_name = ""
        updater_id = ""
        current_time = timezone.localtime()

        if models.Complain.objects.all().count() <= 1 :
            updated_number = 2
        else :
            updated_number = str(int(models.Complain.objects.all().order_by('-number')[0].number) + 1)

        if anonymous_check == "True" or request.user.is_authenticated == False :
            updater_name = "anonymous"
            updater_id = "00000000"
        else :
            updater_name = request.user.username
            updater_id = request.user.user_data.std_year
        models.Complain.objects.create(username = updater_name, updated_text = request.POST['updated_text'], updated_date = current_time, is_anonymous = anonymous_check, number = updated_number)
        logger.info('컴플레인 : [익명여부 :' + anonymous_check +'이름:'+updater_name+'| 학번:'+updater_id+'| 컴플레인 번호:' + str(updated_number) + '] 업로드 완료') # 담당자:{}
        return redirect('login:main')
    else : 
        return redirect('login:main')

def LendUn(request) :
    unbrella_set = models.Unbrella.objects.all()
    battery_set = models.Battery.objects.all()
    lan_set = models.Lan.objects.all()
    post_q = models.Poster.objects.all().order_by('number')
    unbrella_count = unbrella_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    battery_count = battery_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    lan_count = lan_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
    message = ""
    yes_no = False
    manager = models.now_time_table.objects.all()    

    if(models.Unbrella.objects.filter(borrowed_by = request.user.user_data.id).count() > 0) :
        message = "현재 예약하신 우산이 이미 존재합니다."
        yes_no = True
        return render(request, 'login/home.html', {
            'message': message,
            'yes_no': yes_no,
            'battery_count': battery_count,
            'unbrella_count': unbrella_count,
            'lan_count': lan_count,
            'posts':post_q,
            'battery_total' : battery_set.count(),
            'unbrella_total': unbrella_set.count(),
            'lan_total': lan_set.count(),
            'manager':manager
        })


    if unbrella_count < unbrella_set.count():
        for item in unbrella_set.order_by('number'):
                if item.is_available():
                    break
        item.borrowed_by = request.user.user_data
        item.is_reserved = True
        item.reservation_time = timezone.localtime()
        item.save()
        logger.info('우산 사업 : [학번:'+request.user.username+'|우산 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
        return redirect('login:main')
    else :
        messages.add_message(request, messages.INFO, '현재 예약 가능한 우산이 없습니다.')
        yes_no = True

    return render(request, 'login/main_lendunbrella.html', {
        'messages': messages,
        'yesno': yes_no,
        'battery_count':battery_count,
        'lan_count':lan_count,
        'posts':post_q,
        'battery_total' : battery_set.count(),
        'unbrella_total': unbrella_set.count(),
        'lan_total': lan_set.count(),
        'manager':manager
        })


def create_all_password(request):
    player_q = models.User.objects.all().filter(is_superuser = 0)
    cur_time = timezone.localtime()
    for player in player_q :
        player.set_password(player.email)
        player.date_joined = cur_time
        player.save()
    return redirect('login:main') 


def EveryHourStudyTable(request):
    cur_hour = timezone.localtime().hour
    if cur_hour < 20 and cur_hour > 9:
        time_q = models.StudyTable.objects.all().filter(start_time__lte = cur_hour).update(is_borrowed = True)
    return redirect('login:main')


def EveryDayStudyTable(request):
    time_q = models.StudyTable.objects.all()
    time_q.update(is_borrowed = False)
    time_q.update(lender = None)
    return redirect('login:main')



def GetNowManager(request) :
    models.now_time_table.objects.all().delete()
    current_time = timezone.localtime() + datetime.timedelta(minutes=10)
    cur_day = timezone.localtime().weekday()
    num = (current_time.hour - 10) * 2
    if current_time.minute > 30 :
        num = num + 1
    now_manager = models.time_table.objects.all().filter(start_time = num).filter(week_day = cur_day)
    if now_manager.count() == 0 :
        models.now_time_table.objects.create(name='blank', start_time = num, is_manager = False)    

    if now_manager.count() == 1 :
            models.now_time_table.objects.create(name=now_manager.name, start_time = num, is_manage = True)

    if  now_manager.count() > 1 or  now_manager.count() < 0  : ## 오류 상황
        models.now_time_table.objects.create(name='blank', start_time = num, is_manager = False) 
    return redirect('login:main')




def EveryDayErrorCheck (request):
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


    if(studytable_q.count() != studytable_count):
        print("Server Error : 중복된 실습실 레코드가 존재합니다. Admin 사이트에서 이를 직접 관리하거나 서버 관리자에게 문의해주세요")

    return redirect('login:main')


def EveryHourStudyTable(request):
    cur_hour = timezone.localtime().hour
    update_dic = {'is_borrowed' : True, 'lender' : None}
    if cur_hour < 20 and cur_hour > 9:
        time_q = models.StudyTable.objects.all().filter(start_time__lte = cur_hour).update(**update_dic)
    return redirect('login:main')


class first_login_class(PasswordChangeView) :
    def form_valid(self, form):
        date = timezone.localtime()
        self.request.user.date_joined = date
        self.request.user.save()
        return super().form_valid(form)

def password_reset(request) :
    status = 0
    if request.method == "POST" :
        user_id = request.POST.get('user_id')
        tel_num = request.POST.get('tel_num')
        target = models.User.objects.all().filter(username = user_id)
        if target.count() == 1 :
            player = target.first()
            if player.email == tel_num :
                player.set_password(player.email)
                return redirect('login:change_done')
            else :
                status = 2
        else :
            status = 1
    return render(request, 'login/find_pw.html', {'status' : status})


from django.shortcuts import render_to_response
from django.template import RequestContext

def page_not_found(request) :
    response = render_to_response('login/404.html', {}, 
    conttext_instance=RequestContext(request))
    response.status_code = 404
    return response