from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .models import StudyTable
from .forms import UserForm
from .forms import TableForm
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def Main(request):
    return render(request, 'login/final_main.html')



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


def TableLend(request):
    tables = StudyTable.objects.all()
    return render(request, 'login/place_reservation.html', {'tables':tables})

def TableSelect(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            selected_number = request.POST['selected_table']
            table_q = StudyTable.objects.all().filter(number=selected_number)
            return render(request, 'login/place_reservation.html', {'tables' : table_q})
    else:
        form = TableForm()
        return render(request, 'login/place_reservation.html', {'form': form})

def testsel(request):
    if request.method == "POST":
        sel_time = request.POST.getlist('time[]')
        sel_table = request.POST.getlist('number[]')
        table_q = StudyTable.objects.all().filter(start_time__in=sel_time).filter(number__in=sel_table)
        for sel in table_q:
                sel.is_borrowed = True
                sel.lender = request.user.user_data
                sel.save()
        return render(request, 'login/place_reservation.html', {'tables':table_q})
    else:
        form = TimeForm()
        return render(request, 'login/place_reservation.html', {'form' : form})


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


