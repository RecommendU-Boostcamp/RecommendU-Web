from django.shortcuts import render, get_list_or_404, get_object_or_404
from services.models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType, JobList

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .models import RecommendLog, AnswerLog
from services.models import Company, JobSmall, QuestionType
from rest_framework import status
from django.contrib.auth import get_user_model


# Create your views here.
@api_view(['POST'])
def answerlog(request):
    data = request.data
    user = get_object_or_404(get_user_model(), username=data['userId'])
    rec_type = get_object_or_404(RecommendType, rectype_id=int(data['recType']))
    answer = get_object_or_404(Answer, answer_id=data['contentId'])

    instance = AnswerLog(
        user=user,
        answer=answer,
        rectype=rec_type
    )
    
    instance.save()

    
    return Response(status.HTTP_201_CREATED)


@api_view(['POST'])
def recbuttonlog(request):
    data = request.data
    user = get_object_or_404(get_user_model(), username=data['userId'])
    company = get_object_or_404(Company, company=data['company'])
    job_small = get_object_or_404(JobSmall, job_small_id=int(data['jobType']))
    question_type = get_object_or_404(QuestionType, question_type_id=int(data['questionType']))
    question_content = data['questionContent']
    
    
    instance = RecommendLog(
        user=user,
        company=company,
        job_small=job_small,
        question_type=question_type,
        question_from_user=question_content
    )
    instance.save()
    return Response(status.HTTP_201_CREATED)

@api_view(['POST'])
def eval_log(request):
    data = request.data
    user_id = get_object_or_404(get_user_model(), username=data['userId'])
    answer = get_object_or_404(Answer, answer_id=data['contentId'])
    favor = data['favor']
    cnt = data['cnt']
    if favor==1:
        Answer.objects.filter(answer_id=answer.answer_id).update(user_good_cnt=cnt)
    else:
       Answer.objects.filter(answer_id=answer.answer_id).update(user_bad_cnt=cnt)
    return Response(status.HTTP_201_CREATED)