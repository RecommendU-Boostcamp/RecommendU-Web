from django.db import models

class QuestionType(models.Model):
    question_type_id = models.IntegerField(primary_key=True,null=False,unique=True)
    question_type = models.CharField(max_length=100,null=False)
    
class Company(models.Model):
    company_id = models.IntegerField(primary_key=True,null=False,unique=True)
    company = models.CharField(max_length=100,null=False)
    logo_url = models.CharField(max_length=500)

class MajorLarge(models.Model):
    major_large_id = models.IntegerField(primary_key=True,null=False,unique=True)
    major_large = models.CharField(max_length=100,null=False)
    
class MajorSmall(models.Model):
    major_small_id = models.IntegerField(primary_key=True,null=False,unique=True)
    major_large = models.ForeignKey(MajorLarge,related_name="major_smalls",on_delete=models.SET_NULL,null=True)
    major_small = models.CharField(max_length=100,null=False)
    
class JobLarge(models.Model):
    job_large_id = models.IntegerField(primary_key=True,null=False,unique=True)
    job_large = models.CharField(max_length=100,null=False)
    
    def __repr__(self):
        return f'domain name: {self.job_large}, domain id: {self.job_arge_id}'
    
class JobSmall(models.Model):
    job_small_id = models.IntegerField(primary_key=True,null=False,unique=True)
    job_large = models.ForeignKey(JobLarge,related_name="job_smalls",on_delete=models.SET_NULL,null=True)
    job_small = models.CharField(max_length=100,null=False)

class RecommendType(models.Model):
    rectype_id = models.IntegerField(primary_key=True,null=False,unique=True)
    rectype = models.CharField(max_length=100,null=False)
    
class SchoolType(models.Model):
    schooltype_id = models.IntegerField(primary_key=True, null=False, unique=True)
    schooltype = models.CharField(max_length=10, null=False)
    
class Document(models.Model):
    document_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
    company = models.ForeignKey(Company,related_name="documents",on_delete=models.SET_NULL,null=True)
    job_small = models.ForeignKey(JobSmall,related_name="documents",on_delete=models.SET_NULL,null=True)
    major_small = models.ForeignKey(MajorSmall,related_name="documents",on_delete=models.SET_NULL,null=True)
    document_url = models.CharField(max_length=500)
    school = models.ForeignKey(SchoolType, related_name="documents", on_delete=models.SET_NULL, null=True)
    spec = models.CharField(max_length=1000, default=None)
    pro_rating = models.FloatField(null=False)
    
class Answer(models.Model):
    answer_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
    document = models.ForeignKey(Document,related_name="answers",on_delete=models.SET_NULL,null=True)
    content = models.CharField(max_length=10000,null=False)
    question_types = models.ManyToManyField(QuestionType,related_name="answers")
    question = models.CharField(max_length=1000, null=False)
    user_good_cnt = models.IntegerField(default=0)
    user_bad_cnt = models.IntegerField(default=0)
    pro_good_cnt = models.IntegerField(default=0)
    pro_bad_cnt = models.IntegerField(default=0)
    summary = models.CharField(max_length=1000,null=False)
    view = models.IntegerField(default=0)
    user_view = models.IntegerField(default=0)


class Sample(models.Model):
    sample_id = models.CharField(primary_key=True, max_length=10, null=False, unique=True)
    content = models.CharField(max_length=10000,null=False)
    question_type = models.ForeignKey(QuestionType, related_name='samples', on_delete=models.SET_NULL, null=True)
    qeustion = models.CharField(max_length=1000, null=False)
    summary = models.CharField(max_length=1000, null=False)


class ContentList(models.Model):
    answer_id = models.CharField(primary_key=True,max_length=10,null=False,unique=True)
    question = models.CharField(max_length=1000, null=False)
    content = models.CharField(max_length=10000,null=False)
    summary = models.CharField(max_length=1000,null=False)
    spec = models.CharField(max_length=600,null=False)
    schooltype =models.CharField(max_length=100,null=False)
    view = models.IntegerField(default=0)
    user_view = models.IntegerField(default=0)
    document_url = models.CharField(max_length=500)
    company = models.CharField(max_length=100,null=False)
    major_small = models.CharField(max_length=100,null=False)
    job_small = models.CharField(max_length=100,null=False)
    question_types = models.CharField(max_length=200,null=False)
    class Meta:
        managed = False               
        db_table = 'content_view'


class MajorList(models.Model):
    major_large = models.CharField(primary_key=True,max_length=100,null=False)
    major_small = models.CharField(max_length=600,null=False)
    class Meta:
        managed = False               
        db_table = 'major_view'
        
class JobList(models.Model):
    job_large = models.CharField(primary_key=True,max_length=100,null=False)
    job_small = models.CharField(max_length=600,null=False)
    job_small_id = models.CharField(max_length=1000,null=False)
    class Meta:
        managed = False               
        db_table = 'job_view'