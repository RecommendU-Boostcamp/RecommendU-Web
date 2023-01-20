from django.shortcuts import render, get_list_or_404, get_object_or_404
from .dbinit.initiation import dbinit, jobkoreainit, question_type_init, company_init, major_large_init, major_small_init, job_large_init, job_small_init, recommend_type_init, school_init, doc_init, answer_init, sample_init
from .models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType, JobList,Sample

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.db.models import Q

from django.db.models.functions import Length

# Create your views here.

def render_test(request):
    job_query = JobList.objects.all().order_by(Length('job_large').desc())
    question_query = QuestionType.objects.all()[0:21]
    sample_query = {}
    for i in range(1,22):
        question_type = str(1000000+i)
        samples = Sample.objects.filter(question_type_id = question_type)[3:13]
        sample_query[question_type] = [sample.make_sample() for sample in samples] 
    for i in range(0,len(job_query)):
        job_query[i].id = "job_"+str(i)
        job_query[i].job_small = job_query[i].job_small.split(',')
        job_query[i].job_small_id = job_query[i].job_small_id.split(',')
    queryset = ContentList.objects.all()[103:107]
    queryset2 = ContentList.objects.all()[1000:1005]
    queryset3 = ContentList.objects.all()[4000:4003]
    
    companies = Company.objects.all()

    context = {
        "job_list":job_query,
        "answer_list": queryset,
        "answer_list2":queryset2,
        "answer_list3":queryset3,
        "question_type" : question_query,
        'companies' : companies,

        "sample_list" : sample_query,
    }
    return render(request, 'services/index.html', context)


def answer_recommend(request):
    pass


@api_view(['GET', ])
def search_company(request):
    companies = Company.objects.all()
    context = {
        'companies' : companies
    }

    # serializer 달아줘야 함
    return render(request, 'search_test.html', context)


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
