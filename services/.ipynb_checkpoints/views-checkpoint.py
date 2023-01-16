from django.shortcuts import render
from ..jkdata.initiation import dbinit
from .models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer

# Create your views here.

def dbinit(request):
    question_types, companies, major_larges, major_smalls, job_larges, job_smalls, recommend_types = dbinit()
    
    # question_type
    for type in question_types:
        instance = QuestionType()
        instance.question_type = type
        instance.save()
    
    for company in companies:
        instance = Company()
        instance.company = company
    
    for major_large in major_larges:
        instance = MajorLarge()
        instance.large = major_large

    for major_small in major_smalls:
        instance = MajorSmall()
        instance.small = major_small
        
    for job_large in job_larges:
        instance = JobLarge()
        instance.large = job_large

    for job_small in job_smalls:
        instance = JobSmall()
        instance.small = job_small
        
    for recommend_type in recommend_types:
        instance = RecommendType()
        instance.rectype = recommend_type
    

    
    # companies
    # major_larges
    # major_smalls
    # job_larges
    # job_smalls
    # recommend_type
    
    
# class QuestionType(models.Model):
#     question_type_id = models.AutoField(primary_key=True,default=1000001,null=False,unique=True)
#     question_type = models.CharField(max_length=100,null=False)
    
# class Company(models.Model):
#     company_id = models.AutoField(primary_key=True,default=2000001,null=False,unique=True)
#     company = models.CharField(max_length=100,null=False)
#     logo_url = models.CharField(max_length=500)
# class MajorLarge(models.Model):
#     major_large_id = models.AutoField(primary_key=True,default=3000001,null=False,unique=True)
#     major_large = models.CharField(max_length=100,null=False)
    
# class MajorSmall(models.Model):
#     major_small_id = models.AutoField(primary_key=True,default=4000001,null=False,unique=True)
#     major_large = models.ForeignKey(MajorLarge,related_name="major_smalls",on_delete=models.SET_NULL,null=True)
#     major_small = models.CharField(max_length=100,null=False)
    
# class JobLarge(models.Model):
#     job_large_id = models.AutoField(primary_key=True,default=5000001,null=False,unique=True)
#     job_large = models.CharField(max_length=100,null=False)
    
# class JobSmall(models.Model):
#     job_small_id = models.AutoField(primary_key=True,default=6000001,null=False,unique=True)
#     job_large = models.ForeignKey(JobLarge,related_name="job_smalls",on_delete=models.SET_NULL,null=True)
#     job_small = models.CharField(max_length=100,null=False)

# class RecommendType(models.Model):
#     rectype_id = models.AutoField(primary_key=True,default=7000001,null=False,unique=True)
#     rectype = models.CharField(max_length=100,null=False)
    
    
# class Document(models.Model):
#     document_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
#     company = models.ForeignKey(Company,related_name="documents",on_delete=models.SET_NULL,null=True)
#     job_small = models.ForeignKey(JobSmall,related_name="documents",on_delete=models.SET_NULL,null=True)
#     major_small = models.ForeignKey(MajorSmall,related_name="documents",on_delete=models.SET_NULL,null=True)
#     question_types = models.ManyToManyField(QuestionType,related_name="documents")
#     document_url = models.CharField(max_length=500)
#     pro_rating = models.FloatField(null=False)
    
# class Answer(models.Model):
#     answer_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
#     document = models.ForeignKey(Document,related_name="answers",on_delete=models.SET_NULL,null=True)
#     user_good_cnt = models.IntegerField(default=0)
#     user_bad_cnt = models.IntegerField(default=0)
#     pro_good_cnt = models.IntegerField(default=0)
#     pro_bad_cnt = models.IntegerField(default=0)
#     summary = models.CharField(max_length=1000,null=False)
#     view = models.IntegerField(default=0)
#     user_view = models.IntegerField(default=0)