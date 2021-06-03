from __future__ import unicode_literals
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from os.path import dirname, abspath ,join
import pandas as pd
import numpy as np
import csv
d = dirname(dirname(dirname(abspath(__file__)))) #set files directory 
d2 = dirname(dirname(abspath(__file__))) #set files directory 
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
sys.path.insert(1, join(d2,"Preprocess"))
sys.path.insert(1, join(d,"Preparation"))
import Log
import preprocess
import inputPreprocess

# Load Model from file
try:
    with open(join(d,"trained_models","naive_bayes_model.pkl"), 'rb') as filenaive:
        naive_bayes_trained = pickle.load(filenaive)
        Log.log("Naive Bayes Model Loaded Successfully","pretrainedModel.py")
except:
    Log.error("no trained model found for : Naive Bayes - Please train the model first or copy model .pkl file in TrainedModels folder.","pretrainedModel.py")
try:
    with open(join(d,"trained_models","svm_model.pkl"), 'rb') as filesvm:
        svm_trained = pickle.load(filesvm)
        Log.log("SVM Model Loaded Successfully","pretrainedModel.py")
except:
    Log.error("no trained model found for : SVM - Please train the model first or copy model .pkl file in TrainedModels folder.","pretrainedModel.py") 


try:
    transformer = TfidfTransformer()
    loaded_vec = TfidfVectorizer(vocabulary=pickle.load(open(join(d,"trained_models","tfidf_vectorizer_vocab.pkl"), 'rb')))
    Log.log("Vectorizer Loaded Successfully","pretrainedModel.py")
except:
    Log.error("no model found for : Vectorizer - Please train the model first or copy model .pkl file in TrainedModels folder.","pretrainedModel.py") 

'''    
in_text=input("enter your text file address:\n")

f = open(in_text, "r",encoding='utf8')
lines = f.readlines()
file_text=""
for line in lines:
    file_text=file_text+' '+str(line)
f.close()
'''

inputPreprocess.input_preprocess()

with open(join(d,"files",'input_queries_dataset.csv'), 'r', encoding='utf-8',newline='') as csvInputFile:
    csv_reader = csv.reader(csvInputFile, delimiter=',')
    line_count = 0
    counter=0
    for row in csv_reader:
        if line_count<=0:
            line_count+=1
        else:
            preprocessed_input=preprocess.preprocess_input(str(row[0]),transformer,loaded_vec)
            Log.log("Prediction for : "+str(row[0])[0:100]+"...","pretrainedModel.py")
            NBPredict = naive_bayes_trained.predict(preprocessed_input)
            if(NBPredict[0]==0):
                Log.log("--Naive Bayes Result : "+str(NBPredict[0])+" - NOT OFFENSIVE","pretrainedModel.py")
            if(NBPredict[0]==1):
                Log.log("--Naive Bayes Result : "+str(NBPredict[0])+" - OFFENSIVE","pretrainedModel.py")
            SVMPredict = svm_trained.predict(preprocessed_input)
            if(SVMPredict[0]==0):
                Log.log("--SVM Result : "+str(SVMPredict[0])+" - NOT OFFENSIVE","pretrainedModel.py")
            if(SVMPredict[0]==1):
                Log.log("--SVM Result : "+str(SVMPredict[0])+" - OFFENSIVE","pretrainedModel.py")