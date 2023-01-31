from django.shortcuts import render
from services.models import JobList,MajorList
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.db.models.functions import Length
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
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
from rest_framework import status
from rest_framework.response import Response
import json


# Create your views here.

@api_view(['GET', 'POST',])
def login(request):  # GET요청에 대해서는 로그인 페이지를, POST요청에 대해서는 로그인처리를 해주는 함수  
    if request.user.is_authenticated:  # is_authenticated는 식별된 유저라는 뜻
        return redirect('services:main')
    
    if request.method == 'POST':
        try:
            _user = get_object_or_404(get_user_model(), username=request.data['username'])            
        except:
            _user = None            
        if not _user:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        form = AuthenticationForm(request, request.data)
        if form.is_valid():
            auth_login(request, form.get_user())  # user를 로그인함수의 인자로 넣기 위해 불러오는 메소드를 사용해줘야 함
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    context = {
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@api_view(['GET', 'POST', ])
def signup(request):
    if request.method == "POST":        
        # 유저 아이디 중복검사
        try:
            _user = get_object_or_404(get_user_model(), username=request.data['username'])
            
        except:
            _user = None
            
        if _user:
            data = {"message":'같은 아이디가 이미 있습니다.'}
            data = json.dumps(data)
            return Response(data, status=status.HTTP_205_RESET_CONTENT)
        
        if len(request.data['password1']) < 8:
            data = {"message":'비밀번호가 너무 짧습니다.'}
            data = json.dumps(data)
            return Response(data, status=status.HTTP_205_RESET_CONTENT)
        
        if request.data['password1'] != request.data['password2']: 
            data = {"message":'비밀번호가 일치하지 않습니다.'}
            data = json.dumps(data)                      
            return Response(data, status=status.HTTP_205_RESET_CONTENT)

        major_name = request.data.get("major_small")
        major_instance = MajorSmall.objects.get(major_small=major_name)
        job_large_name = request.data.get("interesting_job_large")
        job_large_instance = JobLarge.objects.get(job_large=job_large_name)
        # request.data = request.data.copy()
        request.data["major_small"] = str(major_instance.major_small_id)
        request.data['interesting_job_large'] = str(job_large_instance.job_large_id)
        form = CustomUserCreationForm(request.data)

        if form.is_valid():
            form.save()
            data = {"message": 'Good!'}
            data = json.dumps(data)    
            return Response(data, status=status.HTTP_200_OK)
            # return redirect('services:main')
        
        else:  
            data = {"message": '입력 정보를 다시 한 번 확인하세요.'}
            data = json.dumps(data)       
            return Response(data, status=status.HTTP_205_RESET_CONTENT)
        
    else:
        form = CustomUserCreationForm()  # ModelForm 
        
    jobquery = JobList.objects.all()
    majorquery = MajorList.objects.all().order_by(Length('major_large').desc())
    
    for i in range(0,len(majorquery)):
        majorquery[i].id = "job_"+str(i)
        majorquery[i].major_small = majorquery[i].major_small.split(',')       
         
    context = {
        'form': form,
        "joblist":jobquery,
        "majorlist" : majorquery,
        "majorlist_json" : json.dumps([majors.json() for majors in majorquery])
    }
    return render(request,'accounts/signup.html', context)


@api_view(['POST', ])
def namecheck(request):
    username = request.data['username']
    try:
        _user = get_object_or_404(get_user_model(), username=username)
        
    except:
        _user = None
        
    if _user:
        return Response({"Bad": '이미 사용하는 아이디입니다'}, status=status.HTTP_205_RESET_CONTENT)
    
    else:
        return Response({"Good": '사용할 수 있는 아이디입니다'}, status=status.HTTP_200_OK)

@api_view(["GET"])
def totaluser(request):
    queryset = get_user_model().objects.all()
    serializer = UserSerializer(queryset,many=True)
    return Response(serializer.data)
    

# def signup(request):
#     if request.method == "POST":
#         print(request.POST)
        
#         # 유저 아이디 중복검사
#         try:
#             _user = get_object_or_404(get_user_model(), username=request.POST['username'])
            
#         except:
#             _user = None
            
#         if _user:
#             return Response({'message':'같은 아이디가 이미 있습니다.'}, status=status.HTTP_205_RESET_CONTENT)
        
#         if len(request.POST['password1']) < 8:
#             return Response({'message':'비밀번호가 너무 짧습니다.'}, status=status.HTTP_205_RESET_CONTENT)
        
#         if request.POST['password1'] != request.POST['password2']:
#             return Response({'message':'비밀번호가 일치하지 않습니다.'}, status=status.HTTP_205_RESET_CONTENT)

#         major_name = request.POST.get("major_small")
#         major_instance = MajorSmall.objects.get(major_small=major_name)
#         job_large_name = request.POST.get("interesting-job-large")
#         job_large_instance = JobLarge.objects.get(job_large=job_large_name)
#         request.POST = request.POST.copy()
#         request.POST["major_small"] = str(major_instance.major_small_id)
#         request.POST['interesting-job-large'] = str(job_large_instance.job_large_id)
#         form = CustomUserCreationForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return Response({'message': 'Good!'}, status=status.HTTP_200_OK)
#             # return redirect('services:main')
        
#         else:  
#             print(form.error_messages)
#             return Response({'message': '입력 정보를 다시 한 번 확인하세요.'}, status=status.HTTP_205_RESET_CONTENT)
        
#     else:
#         form = CustomUserCreationForm()  # ModelForm 
        
#     jobquery = JobList.objects.all()
#     majorquery = MajorList.objects.all()
#     for i in range(0,len(majorquery)):
#         majorquery[i].id = "job_"+str(i)
#         majorquery[i].major_small = majorquery[i].major_small.split(',')       
         
#     context = {
#         'form': form,
#         "joblist":jobquery,
#         "majorlist" : majorquery,
#         "majorlist_json" : json.dumps([majors.json() for majors in majorquery])
#     }
#     return render(request,'accounts/signup.html', context)





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


