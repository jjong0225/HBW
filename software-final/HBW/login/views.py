from django.shortcuts import render, get_object_or_404, redirect
from .models import UserInfo
from .forms import UserForm
# Create your views here.

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

def UserShow(request, pk) :
    qs = UserInfo.objects.get(stdID = pk)
    return render(request, 'login/user_show.html', {'user': qs})
