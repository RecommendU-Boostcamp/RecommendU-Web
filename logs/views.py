from django.shortcuts import render, get_list_or_404, get_object_or_404
from services.models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType, JobList

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import RecommendLog, AnswerLog,EvalLog
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
    user = get_object_or_404(get_user_model(), username=data['userId'])
    answer = get_object_or_404(Answer, answer_id=data['contentId'])
    is_contained = EvalLog.objects.filter(user_id=user,answer_id=answer.answer_id)
    favor = data['favor']
    good_cnt = data['goodCnt']
    bad_cnt = data['badCnt']
    count = is_contained.count()
    instance = EvalLog(
        user=user,
        answer=answer,
        favor = favor
    )
    if count == 0:
        if favor==1:
            Answer.objects.filter(answer_id=answer.answer_id).update(user_good_cnt=good_cnt)
        else:
            Answer.objects.filter(answer_id=answer.answer_id).update(user_bad_cnt=bad_cnt)
        instance.save()
        return Response(status.HTTP_201_CREATED)
    else:
        origin = is_contained.values('favor')[0]['favor']
        content = Answer.objects.filter(answer_id=answer.answer_id)
        if origin != favor:
            if favor==1:
                content.update(user_good_cnt=good_cnt)
                content.update(user_bad_cnt = bad_cnt-1)
            else:
                content.update(user_good_cnt=good_cnt-1)
                content.update(user_bad_cnt = bad_cnt)
            EvalLog.objects.filter(user_id=user, answer_id=answer.answer_id).update(favor=favor)
            return Response(status.HTTP_301_MOVED_PERMANENTLY)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)


@api_view(['POST', ])
def user_scrap(request):
    data = request.data
    user = get_object_or_404(get_user_model(), username=data['user_id'])
    answer = get_object_or_404(Answer, answer_id=data['answer_id'])

    try:
        _user = get_object_or_404(get_user_model(), answer_scrap=answer)
    except:
        _user = None
    
    # 만약 스크랩 하지 않았으면 201, 스크랩 했으면 200
    if _user == None:
        answer.scrap_users.add(user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        answer.scrap_users.remove(user)
        return Response(status=status.HTTP_200_OK)