from django.apps import AppConfig
import pandas as pd
import numpy as np
import pickle
from inference.preprocess import FeatureExtractor
import json
from catboost import CatBoostClassifier


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'
    input_answer = pd.read_csv("inference/data/input_answers_1_0.csv")
    with open("inference/data/answer_question_list.pkl", "rb") as file:
        answer_question_types = pickle.load(file)
    document = pd.read_csv("inference/data/jk_documents_3_4.csv")
    item = pd.read_csv("inference/data/jk_answers_without_samples_3_4.csv")
    answer_emb_matrix = np.load("inference/data/answer_embedding_matrix.npy")
    question_emb_matrix = np.load("inference/data/question_embedding_matrix.npy")
    embedder = FeatureExtractor("jhgan/ko-sroberta-multitask")
    cbst = CatBoostClassifier()
    cbst.load_model("inference/models/checkpoint.cbm", format="cbm")

    
    with open("inference/data/question_cate_map_answerid.json", 'r') as f:  #key: question_category, value(list): answer_id
        qcate_dict = json.load(f)
    print("-----------------------------------ALL DATA LOADED-----------------------------------")
