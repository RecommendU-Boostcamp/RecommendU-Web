from django.shortcuts import render, get_list_or_404, get_object_or_404
from ..models import QuestionType, Company, MajorLarge, MajorSmall, JobLarge, JobSmall, RecommendType, Document, Answer, Sample, SchoolType

import numpy as np
import pandas as pd
import json


def dbinit(data_path):
    doc_data = pd.read_csv(data_path+'jk_documents_3_2.csv')

    # question_types
    question_types = ['성장 환경', '전공, 과목', '취미, 특기', '성격의 장/단점', '역량, 강점', 
         '지원동기', '입사 후 포부, 계획, 기여하고 싶은 부분', '프로젝트 경험', '사회 활동, 대외 활동',
         '어려움 극복, 목표 달성 경험', '커뮤니케이션 역량', '어려운 문제를 해결한 경험', '팀워크, 협업(동아리, 팀) 경험', 
         '창의성을 발휘한 경험', '리더쉽을 발휘한 경험', '도전적인 경험', '자유 형식 자기소개', '삶의 가치관', '사회 현상 및 트렌드(최근 뉴스, 국내외 이슈 견해)', 
         '인재상, 기업의 핵심 가치, 기업의 이미지', '경력 사항', '기타', '답변없음']

    # company
    companies = list(doc_data.company.unique())

    # major_large
    major_larges = ['인문/사회계열', '자연/공학/의약계열', '교육계열', '예체능계열', '기타']

    # major_small
    major_smalls = list(doc_data.major_small.unique())

    # job_large
    job_larges = list(doc_data.job_large.unique())

    # job_small
    job_smalls = list(doc_data.job_small.unique())
    
    # schools
    schools = list(doc_data.school.unique())

    # recommendtype은 아직 안정해짐
    recommend_types = ['질문/회사/직무/답변', '질문/직무/답변', '질문/회사/답변', '질문/조회수', '질문/전문가good', '질문/전문가bad']
    
    major_dict = dict(doc_data.groupby('major_small')['major_large'].apply(set).apply(list))
    job_dict = dict(doc_data.groupby('job_small')['job_large'].apply(set).apply(list))
    
    return question_types, companies, major_larges, major_smalls, job_larges, job_smalls, schools, recommend_types, major_dict, job_dict



def jobkoreainit(data_path):
    answer_data = pd.read_csv(data_path+'jk_answers_without_samples_3_2.csv')
    doc_data = pd.read_csv(data_path+'jk_documents_3_2.csv')
    sample_data = pd.read_csv(data_path+'jk_samples_3_2.csv')
    
    return answer_data, doc_data, sample_data




'''
전처리용 함수들
'''
def question_type_init(question_types):
    for i in range(len(question_types)):
        instance = QuestionType()
        instance.question_type_id = 1000000+(i+1)
        instance.question_type = question_types[i]
        instance.save()


def company_init(companies):
    for i in range(len(companies)):
        instance = Company()
        instance.company_id = 2000000+(i+1)
        instance.company = companies[i]
        instance.save()


def major_large_init(major_larges):
    for i in range(len(major_larges)):
        instance = MajorLarge()
        instance.major_large_id = 3000000+(i+1)
        instance.major_large = major_larges[i]
        instance.save()
    
def major_small_init(major_smalls, major_dict):
    for i in range(len(major_smalls)):
        instance = MajorSmall()
        instance.major_small_id = 4000000+(i+1)
        instance.major_small = major_smalls[i]
        instance.major_large = get_object_or_404(MajorLarge, major_large=major_dict[major_smalls[i]][0])
        instance.save()


def job_large_init(job_larges):
    for i in range(len(job_larges)):
        instance = JobLarge()
        instance.job_large_id = 5000000+(i+1)
        instance.job_large = job_larges[i]
        instance.save()


def job_small_init(job_smalls, job_dict):
    for i in range(len(job_smalls)):
        instance = JobSmall()
        instance.job_small_id = 6000000+(i+1)
        instance.job_small = job_smalls[i]
        instance.job_large = get_object_or_404(JobLarge, job_large=job_dict[job_smalls[i]][0])
        instance.save()
        

def recommend_type_init(recommend_types):
    for i in range(len(recommend_types)):
        instance = RecommendType()
        instance.rectype_id = 7000000+(i+1)
        instance.rectype = recommend_types[i]
        instance.save()


def school_init(schools):       
    for i in range(len(schools)):
        instance = SchoolType()
        instance.schooltype_id = 8000000+(i+1)
        instance.schooltype = schools[i]
        instance.save() 
        
    
def doc_init(doc_data):
    n_doc = len(doc_data)
    for i in range(n_doc):
        doc = doc_data.iloc[i]
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

def answer_init(answer_data):
    n_answer = len(answer_data)

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
            
            
def sample_init(sample_data):
    n_sample = len(sample_data)

    for i in range(n_sample):
        sample = sample_data.loc[i]
        instance = Sample()
        instance.sample_id = 's'+str(i).zfill(6)
        instance.question = sample.question
        instance.content = sample.slice_answer
        instance.summary = sample.summary

        qtype = json.loads(sample.sample_category)[0]
        instance.question_type = get_object_or_404(QuestionType, question_type_id=1000000+qtype)
        instance.save()