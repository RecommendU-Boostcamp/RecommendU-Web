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
from services.models import ContentList
from services.serializers import ContentListSerializer
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
        print(request)
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


@api_view(["POST"])
def update(request):
    if request.method == 'POST':
        major_name = request.data.get("major_small")
        major_instance = MajorSmall.objects.get(major_small=major_name)
        job_large_name = request.data.get("interesting_job_large")
        job_large_instance = JobLarge.objects.get(job_large=job_large_name)
        request.data["major_small"] = str(major_instance.major_small_id)
        request.data['interesting_job_large'] = str(job_large_instance.job_large_id)
        user_change_form = CustomUserChangeForm(data=request.data, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", ])
def change_password(request):
    form = PasswordChangeForm(request.user, request.data)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def totaluser(request):
    queryset = get_user_model().objects.all()
    serializer = UserSerializer(queryset,many=True)
    return Response(serializer.data)


def login_test(request):
    context = {"context":"hello"}
    return render(request, 'login.html',context)


@api_view(["POST"])
def myscrap(request):
    user = request.user
    scrap_answers = user.answer_scrap.all()
    scrap_list = []
    for contents in scrap_answers:
        scrap_list.append(contents.answer_id)
    scrap_data = ContentList.objects.filter(answer_id__in=scrap_list)
    serializer = ContentListSerializer(scrap_data, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def myinfo(request):
    user = request.user
    user_info = {
        'id':user.username,
        'major_large':user.major_small.major_large.major_large,
        'major_small':user.major_small.major_small,
        'interesting_job_large':user.interesting_job_large.job_large,
        'career_type':user.career_type
        }
    return Response(user_info)
    
    
def mypage(request):
    jobquery = JobList.objects.all()
    majorsmall_list = MajorSmall.objects.all()
    majorquery = MajorList.objects.all().order_by(Length('major_large').desc())
    
    for i in range(0,len(majorquery)):
        majorquery[i].id = "job_"+str(i)
        majorquery[i].major_small = majorquery[i].major_small.split(',')       
         
    context = {
        "joblist":jobquery,
        "majorsmall_list": majorsmall_list,
        "majorlist" : majorquery,
        "majorlist_json" : json.dumps([majors.json() for majors in majorquery])
    }
    return render(request, 'accounts/mypage.html',context)

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


