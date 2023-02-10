import numpy as np
import pandas as pd


def dbinit(data_path):
    answer_data = pd.read_csv(data_path+'answer_data_2_4.csv')
    doc_data = pd.read_csv(data_path+'document_data_2_4.csv')

    # question_types
    question_types = ['성장환경', '전공, 과목', '취미, 특기', '성격의 장/단점', '역량, 강점', 
         '지원동기', '입사 후 포부, 계획, 기여하고 싶은 부분', '프로젝트 경험', '사회활동',
         '어려움 극복, 목표 달성 경험', '의사소통', '문제 해결', '팀워크, 협업(동아리, 팀) 경험', 
         '창의성', '리더쉽 발휘', '도전', '자기소개', '가치관', '사회 현상 및 트렌드(최근 뉴스, 국내외 이슈 견해)', 
         '인재상, 기업의 핵심 가치, 기업의 이미지', '경력', '기타']

    # company
    companies = list(doc_data.company.unique())

    # major_large
    major_larges = list(doc_data.major_large.unique())

    # major_small
    major_smalls = list(doc_data.major_small.unique())

    # job_large
    job_larges = list(doc_data.job_type.unique())

    # job_small
    job_smalls = list(doc_data.job.unique())

    # recommendtype은 아직 안정해짐
    recommend_types = []
    
    major_dict = dict(doc_data.groupby('major_small')['major_large'].apply(set).apply(list))
    job_dict = dict(doc_data.groupby('job')['job_type'].apply(set).apply(list))
    
    return question_types, companies, major_larges, major_smalls, job_larges, job_smalls, recommend_types, major_dict, job_dict



def jobkoreainit(data_path):
    answer_data = pd.read_csv(data_path+'answer_data_2_4.csv')
    doc_data = pd.read_csv(data_path+'document_data_2_4.csv')
    n_user = 
    
    # 문서를 key로, 전문가 평점을 value로 가짐
    doc_pro_rating = answer_data.groupby('user_id')['score'].apply(set).apply(list)

    
    # 