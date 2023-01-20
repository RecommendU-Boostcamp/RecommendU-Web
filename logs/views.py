from django.shortcuts import render, get_list_or_404, get_object_or_404
from services.models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType, JobList

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse


# Create your views here.
def answerlog(request):
    # request에 어떻게 보낼지에 따라서 달라짐
    pass

@api_view(['POST'])
def recbuttonlog(request):
    user_id = request.POST.get('userid')
    company = request.POST.get('company')
    job_type =request.POST.get('job_type')
    question_type = request.POST.get('question_type')
    print(user_id,company,job_type,question_type)
    return 0