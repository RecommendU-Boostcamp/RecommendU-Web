from rest_framework import serializers
from .models import (
    QuestionType, Company, MajorLarge, MajorSmall,
    JobLarge, JobSmall, RecommendType, SchoolType, 
    Document, Answer, Sample, ContentList,AnswerList,
    DocumentRefreshList,AnswerRefreshList
)

class QuestionTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionType
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = ('company_id', 'company')
    
    
class MajorSmallSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MajorSmall
        fields = '__all__'  # major_large가 자동으로 serialize되는지 한 번만 확인
        

class MajorLargeSerializer(serializers.ModelSerializer):
    major_smalls = MajorSmallSerializer(many=True, read_only=True)
    
    class Meta:
        model = MajorLarge
        fields = '__all__'


class JobSmallTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSmall
        fields = '__all__'

        
class JobLargeSerializer(serializers.ModelSerializer):
    job_smalls = JobSmallTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobLarge
        fields = '__all__'
        
        
class RecommendTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecommendType
        fields = '__all__'
        
        
class SchoolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionType
        fields = '__all__'
    
    
class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnswerList
        fields = ("answer_id","user_good_cnt","user_bad_cnt","pro_good_cnt","pro_bad_cnt","view","user_view","document_id","user_impression_cnt","question_types")
        
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        
        

class ContentListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContentList
        fields = '__all__'
        
class DocumentRefreshSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentRefreshList
        fields = '__all__'
        
class AnswerRefreshSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerRefreshList
        fields = '__all__'