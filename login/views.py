from django.shortcuts import render, get_object_or_404, redirect
from login.models import Student, StudyTable
from login import models
from login.forms import UserForm, TableForm, TimeForm, PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.db.models import Q
import logging
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

    if request.method == "POST":
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
                    logger.info('우 사업 : [학번:'+request.user.username+'|우산 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
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
    })

#마이페이지
@login_required
def MyPage(request):
    current_user = request.user
    cur_time = timezone.localtime()
    after_time = cur_time + timezone.timedelta(minutes=10)

    if request.method == "POST":
        cur_time = request.POST.get('cancel')
        time_q = StudyTable.objects.all().filter(lender_id=current_user.user_data.id).filter(start_time=cur_time)
        for time in time_q:
                time.is_borrowed = False
                time.lender_id = None
                time.save()
        time_q = StudyTable.objects.all().filter(lender_id=current_user.user_data.id)
        return HttpResponse("취소 되었습니다.")
    else:
        time_q = StudyTable.objects.all().filter(lender_id=current_user.user_data.id)
        return render(request, 'login/mypage.html', {'times' : time_q, 'cur_time' : cur_time, 'after_time' : after_time})


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


    def LendTable(request):
        sel_num = request.GET.get('table')
        table_q = StudyTable.objects.all().filter(number=sel_num)
        return render(request, 'login/place_reservation.html', { 'tables' : table_q})
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



<<<<<<< HEAD
=======
class LendBusinessClass() :
    #우산대여
    @login_required
    def LendUnbrella(request):
        unbrella_set = models.Unbrella.objects.all()
        battery_set = models.Battery.objects.all()
        lan_set = models.Lan.objects.all()
        post_q = models.Poster.objects.all().order_by('number')
        unbrella_count = unbrella_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        battery_count = battery_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        lan_count = lan_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        message = ""
        yes_no = False
        ans=request.POST.get('ans', 'No')
        if unbrella_count < unbrella_set.count():
            for item in unbrella_set:
                    if item.is_available():
                        break
            if request.method == "GET":
                message = str(item.number)+"번 우산을 예약하시겠습니까?"
                yes_no = True
            else :
                if ans=='Yes':
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('우산 사업 : [학번:'+request.user.username+'|우산 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                return redirect('login:main')
        else :
            message = "현재 예약 가능한 우산이 없습니다."
            if ans=="OK":
                return redirect('login:main')
            yes_no = False

        return render(request, 'login/main_lendunbrella.html', {
            'message': message,
            'yesno': yes_no,
            'battery_count':battery_count,
            'lan_count':lan_count,
            'posts':post_q,
            'battery_total' : battery_set.count(),
            'unbrella_total': unbrella_set.count(),
            'lan_total': lan_set.count(),
            })

    #배터리대여
    @login_required
    def LendBattery(request):
        unbrella_set = models.Unbrella.objects.all()
        battery_set = models.Battery.objects.all()
        lan_set = models.Lan.objects.all()
        post_q = models.Poster.objects.all().order_by('number')
        unbrella_count = unbrella_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        battery_count = battery_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        lan_count = lan_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        message = ""
        yes_no = False
        ans=request.POST.get('ans', 'No')
        if battery_count < battery_set.count():
            for item in battery_set:
                    if item.is_available() :
                        break
            if request.method == "GET":
                message = str(item.number)+"번 배터리를 빌리시겠습니까?"
                yes_no = True
            else :
                if ans=='Yes':
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('배터리 사업 : [학번:'+request.user.username+'| 배터리 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                return redirect('login:main')
        else :
            message = "현재 예약 가능한 배터리가 없습니다."
            if ans=="OK":
                return redirect('login:main')
            yes_no = False

        return render(request, 'login/main_lendbattery.html', {
            'message': message,
            'yesno': yes_no,
            'lan_count':lan_count,
            'posts':post_q,
            'unbrella_count':unbrella_count,
            'battery_total' : battery_set.count(),
            'unbrella_total': unbrella_set.count(),
            'lan_total': lan_set.count(),
            })

    #랜선대여
    @login_required
    def LendLan(request):
        unbrella_set = models.Unbrella.objects.all()
        battery_set = models.Battery.objects.all()
        lan_set = models.Lan.objects.all()
        post_q = models.Poster.objects.all().order_by('number')
        unbrella_count = unbrella_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        battery_count = battery_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        lan_count = lan_set.filter(Q(is_borrowed = True) | Q(is_reserved = True)).count()
        message = ""
        yes_no = False
        ans=request.POST.get('ans', 'No')
        if lan_count < lan_set.count():
            for item in lan_set:
                    if item.is_available() :
                        break
            if request.method == "GET":
                message = str(item.number)+"번 랜선을 빌리시겠습니까?"
                yes_no = True
            else :
                if ans=='Yes':
                    item.borrowed_by = request.user.user_data
                    item.is_reserved = True
                    item.reservation_time = timezone.localtime()
                    item.save()
                    logger.info('랜선 사업 : [학번:'+request.user.username+'| 랜선 번호:'+str(item.number)+'] 대여 완료') # 담당자:{}
                return redirect('login:main')
        else :
            message = "현재 예약 가능한 랜선이 없습니다."
            if ans=="OK":
                return redirect('login:main')
            yes_no = False
        return render(request, 'login/main_lendlan.html', {
            'message': message,
            'yesno': yes_no,
            'unbrella_count':unbrella_count,
            'battery_count':battery_count,
            'posts':post_q,
            'battery_total' : battery_set.count(),
            'unbrella_total': unbrella_set.count(),
            'lan_total': lan_set.count(),
            })

   

>>>>>>> 9b6f01c94b85252de394d20d63bdcdb9887a28fa

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
    success_url = reverse_lazy('login:main')
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
        if anonymous_check == "True" :
            updater_name = "anonymous"
            updater_id = "00000000"
        else :
            updater_name = request.user.username
            updater_id = request.user.user_data.std_year
        models.Complain.objects.create(username = updater_name, updated_text = request.POST['updated_text'], updated_date = current_time, is_anonymous = anonymous_check, number = updated_number)
        logger.info('컴플레인 : [익명여부 :' + anonymous_check +'이름:'+updater_name+'| 학번:'+updater_id+'| 컴플레인 번호:' + str(updated_number) + '] 업로드 완료') # 담당자:{}
        return render(request, 'login/Test_for_jong.html')
    else : 
        return render(request, 'login/Test_for_jong.html')

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
        })


def create_all_password(request):
    player_q = models.User.objects.all().filter(is_superuser = 0)
    for player in player_q :
        player.set_password(player.email)
        player.save()
    return redirect('login:main') 