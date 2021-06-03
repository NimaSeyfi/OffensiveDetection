from __future__ import unicode_literals
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from os.path import dirname, abspath ,join
import matplotlib.pyplot as plt
import pickle
d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
sys.path.insert(1, join(d,"main"))
import Log
from Preprocess.preprocess import preprocess
from Train.train import fit

#get data from preprocess part
Train_X_Tfidf, Train_Y , Test_X_Tfidf , Test_Y = preprocess(dataset="Dataset_mini.csv")

#training
fit(train_x=Train_X_Tfidf, train_y=Train_Y,
     test_x=Test_X_Tfidf, test_y=Test_Y, 
     save_model=True, plotting=True, 
     print_out=True, models="ALL")


