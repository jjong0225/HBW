from django.shortcuts import render, get_object_or_404, redirect
from login.models import Student, StudyTable
from login import models
from login.forms import UserForm, TableForm, TimeForm, PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from urllib.parse import urlparse, urlunparse

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
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



def Main(request):
    unbrella_set = models.Unbrella.objects.all()
    battery_set = models.Battery.objects.all()
    lan_set = models.Lan.objects.all()
    post_q = models.Poster.objects.all().order_by('number')
    unbrella_count = 0
    battery_count = 0
    lan_count = 0
    
    
    for item in unbrella_set:
        if item.is_borrowed:
            unbrella_count = unbrella_count + 1
    for item in battery_set:
        if item.is_borrowed:
            battery_count = battery_count + 1
    for item in lan_set:
        if item.is_borrowed:
            lan_count = lan_count + 1
    

    return render(request, 'login/final_main.html', {
        'battery_count': battery_count,
        'unbrella_count': unbrella_count,
        'lan_count': lan_count,
        'posts':post_q,
        'battery_total' : battery_set.count(),
        'unbrella_total': unbrella_set.count(),
        'lan_total': lan_set.count(),
    })



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



def TableLend(request):
    tables = StudyTable.objects.all()
    return render(request, 'login/place_reservation.html', {'tables':tables})

def TableSelect(request):
    if request.method == "POST":
        if request.POST.get('desk') is not None:
            selected_number = request.POST['desk']
            table_q = StudyTable.objects.all().filter(number=selected_number)
            return render(request, 'login/place_reservation.html', {'tables' : table_q})
        else:
            form = TableForm()
            return render(request, 'login/place_reservation.html', {'form': form})            
    else:
        form = TableForm()
        return render(request, 'login/place_reservation.html', {'form': form})

def LendTable(request):
    if request.method == "POST":
        sel_time = request.POST.getlist('time[]')
        sel_table = request.POST.getlist('number[]')
        table_q = StudyTable.objects.all().filter(start_time__in=sel_time).filter(number__in=sel_table)
        for sel in table_q:
                sel.is_borrowed = True
                sel.lender = request.user.user_data
                sel.save()
        return redirect('login:seltable')
    else:
        form = TimeForm()
        return render(request, 'login/place_reservation.html', {'form' : form})



#마이페이지
@login_required
def MyPage(request):
    current_user = request.user
    if request.method == "POST":
        sel_time = request.POST.get('cancel')
        cur_time = sel_time[4:]
        time_q = StudyTable.objects.all().filter(lender_id=current_user.id).filter(start_time=cur_time)
        for time in time_q:
                time.is_borrowed = False
                time.lender_id = None
                time.save()
        time_q = StudyTable.objects.all().filter(lender_id=current_user.id)
        return render(request, 'login/mypage.html', {'times' : time_q})
    else:
        time_q = StudyTable.objects.all().filter(lender_id=current_user.id)
        return render(request, 'login/mypage.html', {'times' : time_q})

#우산대여
@login_required
def LendUnbrella(request):
    unbrella_set = models.Unbrella.objects.all()
    battery_set = models.Battery.objects.all()
    lan_set = models.Lan.objects.all()
    unbrella_count = 0
    battery_count = 0
    lan_count = 0
    for unbrella in unbrella_set:
        if unbrella.is_borrowed:
            unbrella_count = unbrella_count + 1
    for item in battery_set:
        if item.is_borrowed:
            battery_count = battery_count + 1
    for item in lan_set:
        if item.is_borrowed:
            lan_count = lan_count + 1

    ans=request.POST.get('ans', 'No')
    if unbrella_count < unbrella_set.count():
        for item in unbrella_set:
                if not item.is_borrowed:
                    break
        if request.method == "GET":
            message = str(item.number)+"번 우산을 빌리시겠습니까?"
            return render(request, 'login/main_lendunbrella.html', {
                'message': message,
                'yesno':True,
                'battery_count':battery_count,
                'lan_count':lan_count,
                'battery_total' : battery_set.count(),
                'unbrella_total': unbrella_set.count(),
                'lan_total': lan_set.count(),
            })
        else :
            if ans=='Yes':
                item.borrowed_by = request.user.user_data
                item.is_borrowed = True
                item.save()
            return redirect('login:main')
    else :
        message = "현재 대여 가능한 우산이 없습니다."
        if ans=="OK":
            return redirect('login:main')
        return render(request, 'login/main_lendunbrella.html', {
            'message': message,
            'yesno': False,
            'battery_count':battery_count,
            'lan_count':lan_count,
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
    unbrella_count = 0
    battery_count = 0
    lan_count = 0
    for unbrella in unbrella_set:
        if unbrella.is_borrowed:
            unbrella_count = unbrella_count + 1
    for item in battery_set:
        if item.is_borrowed:
            battery_count = battery_count + 1
    for item in lan_set:
        if item.is_borrowed:
            lan_count = lan_count + 1
    ans=request.POST.get('ans', 'No')
    if battery_count < battery_set.count():
        for item in battery_set:
                if not item.is_borrowed:
                    break
        if request.method == "GET":
            message = str(item.number)+"번 배터리를 빌리시겠습니까?"
            return render(request, 'login/main_lendbattery.html', {
                'message': message,
                'yesno':True,
                'lan_count':lan_count,
                'unbrella_count':unbrella_count,
                'battery_total' : battery_set.count(),
                'unbrella_total': unbrella_set.count(),
                'lan_total': lan_set.count(),
            })
        else :
            if ans=='Yes':
                item.borrowed_by = request.user.user_data
                item.is_borrowed = True
                item.save()
            return redirect('login:main')
    else :
        message = "현재 대여 가능한 배터리가 없습니다."
        if ans=="OK":
            return redirect('login:main')
        return render(request, 'login/main_lendbattery.html', {
            'message': message,
            'yesno': False,
            'lan_count':lan_count,
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
    unbrella_count = 0
    battery_count = 0
    lan_count = 0
    for unbrella in unbrella_set:
        if unbrella.is_borrowed:
            unbrella_count = unbrella_count + 1
    for item in battery_set:
        if item.is_borrowed:
            battery_count = battery_count + 1
    for item in lan_set:
        if item.is_borrowed:
            lan_count = lan_count + 1

    ans=request.POST.get('ans', 'No')
    if lan_count < lan_set.count():
        for item in lan_set:
                if not item.is_borrowed:
                    break
        if request.method == "GET":
            message = str(item.number)+"번 랜선을 빌리시겠습니까?"
            return render(request, 'login/main_lendlan.html', {
                'message': message,
                'yesno':True,
                'unbrella_count':unbrella_count,
                'battery_count':battery_count,
                'battery_total' : battery_set.count(),
                'unbrella_total': unbrella_set.count(),
                'lan_total': lan_set.count(),
            })
        else :
            if ans=='Yes':
                item.borrowed_by = request.user.user_data
                item.is_borrowed = True
                item.save()
            return redirect('login:main')
    else :
        message = "현재 대여 가능한 랜선이 없습니다."
        if ans=="OK":
            return redirect('login:main')
        return render(request, 'login/main_lendlan.html', {
            'message': message,
            'yesno': False,
            'unbrella_count':unbrella_count,
            'battery_count':battery_count,
            'battery_total' : battery_set.count(),
            'unbrella_total': unbrella_set.count(),
            'lan_total': lan_set.count(),
            })


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
    success_url = reverse_lazy('password_change_done')
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
