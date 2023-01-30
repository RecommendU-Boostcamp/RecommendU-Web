from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .dbinit.initiation import dbinit, jobkoreainit, question_type_init, company_init, major_large_init, major_small_init, job_large_init, job_small_init, recommend_type_init, school_init, doc_init, answer_init, sample_init
from django.contrib.auth import get_user_model

from .models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType, JobList,Sample,AnswerList
from .serializers import ContentListSerializer,DocumentSerializer,AnswerSerializer
from logs.models import EvalLog

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Q

from django.db.models.functions import Length
from services.apps import ServicesConfig
from inference.preprocess import Recommendation
import time
import json
import random

# Create your views here.


@api_view(['POST', ])
def answer_recommend(request):
    # request에 유저가 누군지 + 회사/질문/직무/답변 달려있음
    s_time = time.time()
    data = request.data
    company = get_object_or_404(Company, company=data["company"])
    job_small = get_object_or_404(JobSmall, job_small_id=int(data["jobType"]))
    question_type = get_object_or_404(QuestionType, question_type_id = int(data["questionType"]))
    question_text = data["questionText"]
    content = data["content"]
    user = request.user
    
    if question_type.question_type_id == 1000023:
        import re
        WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
        question_text = WHITESPACE_HANDLER(question_text)
        question_category, sim = ServicesConfig.embedder.match_question_top1(question_text, ServicesConfig.question_emb_matrix)
        if len(question_text)==0 or sim < 0.5:
            return Response(status.HTTP_412_PRECONDITION_FAILED)
        question_category +=1000000
        question_type = get_object_or_404(QuestionType, question_type_id = question_category)
    
    if len(content) < 10:
        content = ""
        
    recommend = Recommendation(ServicesConfig.document, ServicesConfig.item, ServicesConfig.qcate_dict, ServicesConfig.answer_emb_matrix, ServicesConfig.embedder, 
                            question_type.question_type_id-1000000, company.company, user.favorite_company, job_small.job_large.job_large, job_small.job_small, content, 
                            4)
    
    recommend.filtering()
    result = {
            " 님과 유사한 자소서를 골라봤어요" : recommend.recommend_with_company_jobtype(),
            "지원하는 회사를 먼저 고려했어요" : recommend.recommend_with_company_without_jobtype(),
            "비슷한 직무로 모아봤어요" : recommend.recommend_with_jobtype_without_company(),
            "조회를 많이 했어요" : recommend.recommed_based_popularity(),
            "전문가 평이 좋아요" : recommend.recommend_based_expert()[0],
            "전문가 평이 별로에요" : recommend.recommend_based_expert()[1]
            }
    
    result_keys = result.keys()
    to_front = {key : [] for key in result_keys}
    
    for key in result:
        ran_num=4
        if key in ["전문가 평이 좋아요", "전문가 평이 별로에요"]:
            ran_num = 2
        for i in range(ran_num):
            temp_answer = get_object_or_404(ContentList, answer_id= 'a'+str(result[key][i]).zfill(6))
            temp_answer = ContentListSerializer(temp_answer)
            to_front[key].append(temp_answer.data)

    return Response(to_front)


@api_view(['POST', ])
def check_status(request):
    data = request.data
    
    user = get_object_or_404(get_user_model(), username=data['user_id'])
    answer = get_object_or_404(Answer, answer_id=data['answer_id'])
    is_good_eval = None
    
    good_count = EvalLog.objects.filter(answer_id=answer, favor=1).count()
    bad_count = EvalLog.objects.filter(answer_id=answer, favor=0).count()
    
    user_eval_list = list(user.answer_eval.all())
    
    try:
        _ = bool(get_object_or_404(get_user_model(), answer_scrap=answer))
        is_scrap = True
    except:
        is_scrap = False
    
    if answer in user_eval_list:
        is_eval = True
        eval_log = get_object_or_404(EvalLog, user_id=user, answer_id=answer)
        eval_status = eval_log.favor
    else:
        is_eval = False
    
    if is_eval:
        result = {"isScrap": is_scrap, "isEval": is_eval, "evalStatus": eval_status, "goodCnt": good_count, "badCnt": bad_count}
    else:
        result = {"isScrap": is_scrap, "isEval": is_eval, "goodCnt": good_count, "badCnt": bad_count}
    
    data = json.dumps(result)
    return Response(data, status=status.HTTP_200_OK)




def main(request):
    if not request.user.is_authenticated:  # 만약 식별된 사용자가 아니면 
        return redirect("accounts:login")
        
    job_query = JobList.objects.all().order_by(Length('job_large').desc())
    question_query = QuestionType.objects.all()[0:21]
    sample_query = {}

    for i in range(1,22):
        question_type = str(1000000+i)
        samples = Sample.objects.filter(question_type_id = question_type)
        result = [json.dumps(sample.make_sample()) for sample in samples]
        random.shuffle(result)
        sample_query[question_type] = result
        
    for i in range(0,len(job_query)):
        job_query[i].id = "job_"+str(i)
        job_query[i].job_small = job_query[i].job_small.split(',')
        job_query[i].job_small_id = job_query[i].job_small_id.split(',')
    
    companies = Company.objects.all().order_by('company')

    context = {
        "job_list":job_query,
        "question_type" : question_query,
        'companies' : companies,
        "sample_list" : sample_query,
    }
    return render(request, 'services/main.html', context)

    


@api_view(['GET', ])
def search_company(request):
    companies = Company.objects.all()
    context = {
        'companies' : companies
    }

    # serializer 달아줘야 함
    return render(request, 'search_test.html', context)




'''
아래의 함수는 데이터베이스에 등록하는 용도이며, 초기화 이후에는 접근 url을 차단합니다.
'''

def db_first(request):
    data_path = '/opt/ml/RecommendU/RecommendU-back/services/dbinit/'
    question_types, companies, major_larges, major_smalls, job_larges, job_smalls, schools, recommend_types, major_dict, job_dict = dbinit(data_path)   
    
    question_type_init(question_types)
    company_init(companies)
    major_large_init(major_larges)
    major_small_init(major_smalls, major_dict)
    job_large_init(job_larges)
    job_small_init(job_smalls, job_dict)
    recommend_type_init(recommend_types)
    school_init(schools)

    return HttpResponse("Init Done!")
 


def docu_answer_init(request):
    data_path = '/opt/ml/RecommendU/RecommendU-back/services/dbinit/'
    answer_data, doc_data, sample_data = jobkoreainit(data_path)

    doc_init(doc_data)
    answer_init(answer_data)
    sample_init(sample_data)

    return HttpResponse(f"cover letter saving Done")

# document, answer 데이터를 model server로 보낼 api
@api_view(["GET"])
def document_total(request):
    queryset = Document.objects.all()
    serializer = DocumentSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def answer_total(request):
    queryset = AnswerList.objects.all()
    serializer = AnswerSerializer(queryset,many=True)
    return Response(serializer.data)