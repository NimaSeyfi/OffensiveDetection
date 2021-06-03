from __future__ import unicode_literals
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score

from os.path import dirname, abspath ,join
import matplotlib.pyplot as plt
import pickle
d = dirname(dirname(dirname(abspath(__file__)))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
print(sys.path)
import Log

'''
####################################################################
###########################LEARNING SECTION#########################
####################################################################
'''

    


def fit(train_x , train_y, test_x, test_y, save_model=True, plotting=False, print_out=True, models="ALL"):
    Log.log("fit process started with parameteres : save_model : "+save_model+" - plotting : "+plotting+" - models : "+models,"train.py")
    if models=="ALL":
        Log.log("starting Naive Bayes training.", "train.py")
        nb_accuarcy=fit_nb(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        Log.log("starting SVM training.", "train.py")
        svm_accuracy=fit_svm(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        
        if plotting:
            #Plotting:
            names = ['Naive Bayes = '+str(nb_accuarcy), 'SVM = '+str(svm_accuracy)]
            values = [nb_accuarcy, svm_accuracy]

            plt.figure(figsize=(9, 3))
            plt.bar(names, values, color=['red','blue'])
            plt.suptitle('Accuracy')
            plt.show()
        return nb_accuarcy, svm_accuracy

    elif models=="NAIVE_BAYES":
        Log.log("starting Naive Bayes training.", "train.py")
        nb_accuarcy = fit_nb(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        return nb_accuarcy

    elif models=="SVM":
        Log.log("starting SVM training.", "train.py")
        svm_accuracy = fit_svm(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        return svm_accuracy

    else:
        Log.error("no model(s) found.", "train.py")
        return null

def fit_svm(train_x , train_y, test_x, test_y, save_model=True,print_out=True):
    #SVM Learning:
    #fitting dataset for SVM Classifier
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(train_x,train_y)
    #Test : Predict for validation
    predictions_SVM = SVM.predict(test_x)
    #Use accuracy_score function to get the accuracy
    svm_accuracy=accuracy_score(predictions_SVM, test_y)*100
    if print_out:
        print("SVM Accuracy Score -> ",svm_accuracy)

    Log.log("SVM model trained with accuarcy : "+svm_accuracy, "train.py")
    # Save SVM to file in the current working directory
    if save_model:
        with open(join(d,"trained_models","svm_model.pkl"), 'wb') as filesvm:
            pickle.dump(SVM, filesvm)
        Log.log("SVM Model Saved to trained_models\svm_model.pkl", "train.py")
    else:
        Log.warning("SVM Model Not Saved, save_model parameter not setted true. unable use pretrained model in feature.", "train.py")

    return svm_accuracy

def fit_nb(train_x , train_y, test_x, test_y, save_model=True,print_out=True):
    #NAIVE BAYES:
    #fitting dataset for NB Classifier
    Naive = naive_bayes.MultinomialNB()
    Naive.fit(train_x,train_y)
    #Test : Predict for validation
    predictions_NB = Naive.predict(test_x)
    #Use accuracy_score function to get the accuracy
    nb_accuarcy=accuracy_score(predictions_NB, test_y)*100

    if print_out:
        print("Naive Bayes Accuracy Score -> ",nb_accuarcy)
    
    Log.log("Naive Bayes model trained with accuarcy : "+nb_accuarcy, "train.py")
    # Save NB to file in the current working directory
    if save_model:
        with open(join(d,"trained_models","naive_bayes_model.pkl"), 'wb') as filenaive:
            pickle.dump(Naive, filenaive)
        Log.log("NB Model Saved to trained_models\\naive_bayes_model.pkl", "train.py")
    else:
        Log.warning("NB Model Not Saved, save_model parameter not setted true. unable use pretrained model in feature.", "train.py")
    
    return nb_accuarcy