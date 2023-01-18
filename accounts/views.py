from django.shortcuts import render
from services.models import JobList,MajorList

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