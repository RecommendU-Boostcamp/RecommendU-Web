from django.shortcuts import render
from services.models import JobList,MajorList

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm, 
    PasswordChangeForm,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.http import HttpResponse
from services.models import MajorSmall, JobLarge


# Create your views here.

def login(request):  # GET요청에 대해서는 로그인 페이지를, POST요청에 대해서는 로그인처리를 해주는 함수  
    if request.user.is_authenticated:
        return redirect('services:render')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())  # user를 로그인함수의 인자로 넣기 위해 불러오는 메소드를 사용해줘야 함
            next_url = request.GET.get('next')
            print("success")
            return redirect(next_url or 'services:render')
        else:
            print("fail form")
    
    else:
        print("fail")
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

# def logout(request):
#     if request.user.is_authenticated:
#         auth_logout(request)
#     return redirect('articles:index')


def signup(request):
    if request.method == "POST":
        major_name = request.POST.get("major_small")
        major_instance = MajorSmall.objects.get(major_small=major_name)
        job_large_name = request.POST.get("interesting_job_large")
        job_large_instance = JobLarge.objects.get(job_large=job_large_name)
        request.POST = request.POST.copy()
        request.POST["major_small"] = str(major_instance.major_small_id)
        request.POST['interesting_job_large'] = str(job_large_instance.job_large_id)
        form = CustomUserCreationForm(request.POST)

        
        if form.is_valid():
            form.save()
            return redirect('services:render')
        
        else:
            return HttpResponse(f'error occur')
        
    else:
        form = CustomUserCreationForm()  # ModelForm 
        
    jobquery = JobList.objects.all()
    majorquery = MajorList.objects.all()
    for i in range(0,len(majorquery)):
        majorquery[i].id = "job_"+str(i)
        majorquery[i].major_small = majorquery[i].major_small.split(',')        

    context = {
        'form': form,
        "joblist":jobquery,
        "majorlist" : majorquery,
    }
    return render(request,'signup.html', context)

# def delete(request):
#     if request.user.is_authenticated:
#         request.user.delete()
#         auth_logout(request)
#     return redirect('articles:index')

# def update(request):
#     if request.method == "POST":
#         form = CustomUserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect ('articles:index')
#     else:
#         form = CustomUserChangeForm(instance=request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/update.html', context)


# def change_password(request):
#     if request.method == "POST":
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             # 1
#             # user = form.save
#             # update_session_auth_hash(request, user)
#             form.save()
#             update_session_auth_hash(request, form.user)
#             redirect('articles:index')
#     else:
#         form = PasswordChangeForm(request.user)  # 새비밀번호/확인은 SetPasswordForm 것이고, PasswordChangeForm은 여기에 기존 비밀번호를 추가한 폼. 
#     context = {
#         'form': form
#     }
#     return render(request, 'accounts/change_password.html', context)



# Create your views here.

def login_test(request):
    context = {"context":"hello"}
    return render(request, 'login.html',context)

def signup_test(request):
    jobquery = JobList.objects.all()
    majorquery = MajorList.objects.all()
    for i in range(0,len(majorquery)):
        majorquery[i].id = "job_"+str(i)
        majorquery[i].major_small = majorquery[i].major_small.split(',')
    context = {
        "joblist":jobquery,
        "majorlist" : majorquery,
    }
    return render(request, 'signup.html',context)


