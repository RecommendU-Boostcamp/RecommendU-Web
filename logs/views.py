from django.shortcuts import render, get_list_or_404, get_object_or_404
from services.models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType, JobList

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .models import RecommendLog, AnswerLog
from services.models import Company, JobSmall, QuestionType
from django.contrib.auth import get_user_model


# Create your views here.
@api_view(['POST'])
def answerlog(request):
    # request에 어떻게 보낼지에 따라서 달라짐
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

    
    return HttpResponse('Done')


@api_view(['POST'])
def recbuttonlog(request):
    data = request.data
    print(data)
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
    return HttpResponse('Done')



# class AnswerLog(models.Model):
#     answer_log_id = models.BigAutoField(primary_key=True,null=False)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=False)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
#     rectype = models.ForeignKey(RecommendType,on_delete=models.SET_NULL,null=True)

# class RecommendLog(models.Model):
#     rec_log_id = models.BigAutoField(primary_key=True,null=False)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="rec_logs",on_delete=models.CASCADE,null=False)
#     company = models.ForeignKey(Company,related_name="rec_logs",on_delete=models.SET_NULL,null=True)
#     job_small = models.ForeignKey(JobSmall,related_name="rec_logs",on_delete=models.SET_NULL,null=True)
#     question_type = models.ForeignKey(QuestionType,related_name="rec_logs",on_delete=models.SET_NULL,null=True)