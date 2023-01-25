from django.apps import AppConfig
import pandas as pd
import numpy as np
from inference.preprocess import FeatureExtractor
import json


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'
    document = pd.read_csv("inference/data/jk_documents_3_2.csv")
    item = pd.read_csv("inference/data/jk_answers_without_samples_3_2.csv")
    answer_emb_matrix = np.load("inference/data/answer_embedding_matrix.npy")
    question_emb_matrix = np.load("inference/data/question_embedding_matrix.npy")
    embedder = FeatureExtractor("jhgan/ko-sroberta-multitask")
    
    with open("inference/data/question_cate_map_answerid.json", 'r') as f:  #key: question_category, value(list): answer_id
        qcate_dict = json.load(f)
    print("-----------------------------------ALL DATA LOADED-----------------------------------")
