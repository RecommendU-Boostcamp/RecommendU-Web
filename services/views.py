from django.shortcuts import render, get_list_or_404, get_object_or_404
from .jkdata.initiation import dbinit, jobkoreainit
from .models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample,ContentList, MajorList, SchoolType,JobList
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .models import Answer
from django.db.models.functions import Length

import json
import ast

# Create your views here.

def render_test(request):
    job_query = JobList.objects.all().order_by(Length('job_large').desc())
    question_query = QuestionType.objects.all()[0:21]
    for i in range(0,len(job_query)):
        job_query[i].id = "job_"+str(i)
        job_query[i].job_small = job_query[i].job_small.split(',')
        job_query[i].job_small_id = job_query[i].job_small_id.split(',')
    queryset = ContentList.objects.all()[103:107]
    queryset2 = ContentList.objects.all()[1000:1005]
    queryset3 = ContentList.objects.all()[4000:4003]
    context = {
        "job_list":job_query,
        "answer_list": queryset,
        "answer_list2":queryset2,
        "answer_list3":queryset3,
        "question_type" : question_query,
    }
    return render(request, 'index.html', context)

def db_first(request):
    data_path = '/opt/ml/RecommendU/RecommendU-back/services/jkdata/'
    question_types, companies, major_larges, major_smalls, job_larges, job_smalls, schools, recommend_types, major_dict, job_dict = dbinit(data_path)
    
    # question_type
    for i in range(len(question_types)):
        instance = QuestionType()
        instance.question_type_id = 1000000+(i+1)
        instance.question_type = question_types[i]
        instance.save()

    for i in range(len(companies)):
        instance = Company()
        instance.company_id = 2000000+(i+1)
        instance.company = companies[i]
        instance.save()
    
    for i in range(len(major_larges)):
        instance = MajorLarge()
        instance.major_large_id = 3000000+(i+1)
        instance.major_large = major_larges[i]
        instance.save()


    for i in range(len(major_smalls)):
        instance = MajorSmall()
        instance.major_small_id = 4000000+(i+1)
        instance.major_small = major_smalls[i]
        instance.save()


    for i in range(len(job_larges)):
        instance = JobLarge()
        instance.job_large_id = 5000000+(i+1)
        instance.job_large = job_larges[i]
        instance.save()


    for i in range(len(job_smalls)):
        instance = JobSmall()
        instance.job_small_id = 6000000+(i+1)
        instance.job_small = job_smalls[i]
        instance.save()


    for i in range(len(recommend_types)):
        instance = RecommendType()
        instance.rectype_id = 7000000+(i+1)
        instance.rectype = recommend_types[i]
        instance.save()
        
        
    for i in range(len(schools)):
        instance = SchoolType()
        instance.schooltype_id = 8000000+(i+1)
        instance.schooltype = schools[i]
        instance.save() 


    # ForeignKey 등록해주는 과정
    for i in range(len(major_smalls)):
        instance = get_object_or_404(MajorSmall, major_small=major_smalls[i])
        instance.major_large = get_object_or_404(MajorLarge, major_large=major_dict[major_smalls[i]][0])
        instance.save()

    for i in range(len(job_smalls)):
        instance = get_object_or_404(JobSmall, job_small=job_smalls[i])
        instance.job_large = get_object_or_404(JobLarge, job_large=job_dict[job_smalls[i]][0])
        instance.save()

    return HttpResponse("Init Done!")
 


def docu_answer_init(request):
    data_path = '/opt/ml/RecommendU/RecommendU-back/services/jkdata/'
    answer_data, doc_data, sample_data = jobkoreainit(data_path)

    n_doc = len(doc_data)
    n_answer = len(answer_data)
    n_sample = len(sample_data)

    for i in range(n_doc):
        doc = doc_data.iloc[i]
        instance = get_object_or_404(Document, document_id='d'+str(doc.doc_id).zfill(6))
        instance = Document()
        instance.document_id ='d'+str(doc.doc_id).zfill(6)
        instance.company = get_object_or_404(Company, company=doc.company)
        instance.job_small = get_object_or_404(JobSmall, job_small=doc.job_small)
        instance.major_small = get_object_or_404(MajorSmall, major_small=doc.major_small)
        instance.document_url = doc.doc_url
        instance.pro_rating = doc.pro_rating
        instance.school = get_object_or_404(SchoolType, schooltype=doc.school)
        instance.spec = doc.extra_spec
        instance.save()

    for i in range(n_answer):
        answer = answer_data.loc[i]
        instance = Answer()
        instance.answer_id = 'a'+str(answer.answer_id).zfill(6)
        instance.content = answer.answer
        instance.question = answer.question
        instance.document = get_object_or_404(Document, document_id='d'+str(answer.doc_id).zfill(6))
        instance.pro_good_cnt = answer.pro_good_cnt
        instance.pro_bad_cnt = answer.pro_bad_cnt
        instance.summary = answer.summary
        instance.view = answer.doc_view
        
        qtypes = json.loads(answer.question_category)
        for qtype in qtypes:
            temp_qtype = get_object_or_404(QuestionType, question_type_id=1000000+qtype)
            instance.question_types.add(temp_qtype)
        instance.save()
    
    for i in range(n_sample):
        sample = sample_data.loc[i]
        instance = Sample()
        instance.sample_id = 's'+str(i).zfill(6)
        instance.question = sample.question
        instance.content = sample.answer
        instance.summary = sample.summary

        qtype = json.loads(sample.sample_category)[0]
        instance.question_type = get_object_or_404(QuestionType, question_type_id=1000000+qtype)
        instance.save()

    return HttpResponse(f"cover letter saving Done")    
