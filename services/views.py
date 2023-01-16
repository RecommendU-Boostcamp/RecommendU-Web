from django.shortcuts import render, get_list_or_404, get_object_or_404
from .jkdata.initiation import dbinit, jobkoreainit
from .models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer
from rest_framework.decorators import api_view
from django.http import HttpResponse

import json

# Create your views here.

# @api_view(['POST'])
def db_first(request):
    data_path = '/opt/ml/RecommendU/RecommendU-back/services/jkdata/'
    question_types, companies, major_larges, major_smalls, job_larges, job_smalls, recommend_types, major_dict, job_dict = dbinit(data_path)
    
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
 
    


def jkinit(request):
    data_path = '/opt/ml/RecommendU/RecommendU-back/services/jkdata/'
    answer_data, doc_data = jobkoreainit(data_path)

    n_doc = len(doc_data)
    n_answer = len(answer_data)

    for i in range(n_doc):
        doc = doc_data.iloc[i]
        instance = Document()
        instance.document_id ='d' + str(doc.doc_id).zfill(6)
        instance.company = get_object_or_404(Company, company=doc.company)
        instance.job_small = get_object_or_404(JobSmall, job_small=doc.job_small)
        instance.major_small = get_object_or_404(MajorSmall, major_small=doc.major_small)
        instance.document_url = doc.doc_url
        instance.pro_rating = doc.pro_rating
        instance.save()

    for i in range(n_answer):
        answer = answer_data.loc[i]
        instance = Answer()
        instance.answer_id = 'a' + str(answer.answer_id).zfill(6)
        instance.pro_good_cnt = answer.pro_good_cnt
        instance.pro_bad_cnt = answer.pro_bad_cnt
        instance.summary = answer.summary
        instance.view = answer.doc_view

        # qtypes = json.loads(answer.question_category)
        # for qtype in qtypes:
        #     temp_qtype = get_object_or_404(QuestionType, question_type_id=qtype)
        #     instance.question_types.add(temp_qtype)
        instance.save()

    return HttpResponse(f"cover letter saving Done")
 





        

# class Answer(models.Model):
#     answer_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
#     document = models.ForeignKey(Document,related_name="answers",on_delete=models.SET_NULL,null=True)
#     user_good_cnt = models.IntegerField(default=0)
#     user_bad_cnt = models.IntegerField(default=0)
#     pro_good_cnt = models.IntegerField(default=0)
#     pro_bad_cnt = models.IntegerField(default=0)
#     question_types = models.ManyToManyField(QuestionType,related_name="answers")
#     summary = models.CharField(max_length=1000,null=False)
#     view = models.IntegerField(default=0)
#     user_view = models.IntegerField(default=0)

# class Document(models.Model):
#     document_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
#     company = models.ForeignKey(Company,related_name="documents",on_delete=models.SET_NULL,null=True)
#     job_small = models.ForeignKey(JobSmall,related_name="documents",on_delete=models.SET_NULL,null=True)
#     major_small = models.ForeignKey(MajorSmall,related_name="documents",on_delete=models.SET_NULL,null=True)
#     document_url = models.CharField(max_length=500)
#     pro_rating = models.FloatField(null=False)
    
