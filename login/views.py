from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import UserForm
from .models import StudyTable
from . import models
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.models import User
# Create your views here.

def Main(request):
    unbrella_set = models.Unbrella.objects.all()
    battery_set = models.Battery.objects.all()
    lan_set = models.Lan.objects.all()
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
    })



# 'name', 'stdID', 'HB'
def Signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/login/final_main/')
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
            return redirect('/login/final_main/')
        else:
            return HttpResponse(user)
    else:
        form = UserForm()
        return render(request, 'login/final_login.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def UserEdit(request, pk):
    user = get_object_or_404(UserInfo, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance = user)
        if form.is_valid() :
            form.save()
            return render(request, 'login/user_edit_detail.html', {'user':user})
    else:
        form = UserForm(instance=user)
    return render(request, 'login/user_edit.html', {'form': form})

@login_required
def UserShow(request, pk) :
    qs = UserInfo.objects.get(stdID = pk)
    return render(request, 'login/user_show.html', {'user': qs})



#마이페이지
@login_required
def MyPage(request):
    return render(request, 'login/mypage.html')

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
    if unbrella_count < 10:
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
    if battery_count < 10:
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
    if lan_count < 10:
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
            })