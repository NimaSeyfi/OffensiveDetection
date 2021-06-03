from __future__ import unicode_literals
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, \
    recall_score, confusion_matrix, classification_report, \
    accuracy_score, f1_score
from os.path import dirname, abspath ,join
import matplotlib.pyplot as plt
import pickle
d = dirname(dirname(dirname(abspath(__file__)))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log

'''
####################################################################
###########################LEARNING SECTION#########################
####################################################################
'''

    


def fit(train_x , train_y, test_x, test_y, save_model=True, plotting=False, print_out=True, models="ALL"):
    Log.log("fit process started with parameteres : save_model : "+str(save_model)+" - plotting : "+str(plotting)+" - models : "+models,"train.py")
    if models=="ALL":
        Log.log("starting Naive Bayes training.", "train.py")
        nb_accuarcy=fit_nb(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        Log.log("starting SVM training.", "train.py")
        svm_accuracy=fit_svm(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        Log.log("starting knn training.", "train.py")
        knn_accuracy=fit_knn(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        
        if plotting:
            #Plotting:
            names = ['Naive Bayes = '+str(nb_accuarcy), 'SVM = '+str(svm_accuracy)
            , 'KNN = '+str(knn_accuracy)]
            values = [nb_accuarcy, svm_accuracy,knn_accuracy]

            plt.figure(figsize=(9, 3))
            plt.bar(names, values, color=['red','blue','green'])
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

    elif models=="KNN":
        Log.log("starting KNN training.", "train.py")
        knn_accuracy = fit_knn(train_x , train_y, test_x, test_y, save_model=save_model,print_out=print_out)
        return knn_accuracy

    else:
        Log.error("no model(s) found.", "train.py")
        return None

def fit_svm(train_x , train_y, test_x, test_y, save_model=True,print_out=True):
    #SVM Learning:
    #fitting dataset for SVM Classifier
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(train_x,train_y)
    #Test : Predict for validation
    predictions_SVM = SVM.predict(test_x)
    #Use accuracy_score function to get the accuracy
    svm_accuracy=accuracy_score(predictions_SVM, test_y)*100
    svm_precision=precision_score(test_y, predictions_SVM)*100
    svm_recall=recall_score(test_y, predictions_SVM)*100
    svm_f1= f1_score(test_y, predictions_SVM, average=None )
    tn, fp, fn, tp = confusion_matrix(test_y, predictions_SVM).ravel()
    fscore = (2*(svm_precision*svm_recall)/(svm_precision+svm_recall))
    fnrate = (fn /len(test_y)) *100
    fprate = (fp /len(test_y)) *100
    print("f-score : "+str(fscore))
    print("fn rate : "+str(fnrate))
    print("fp rate : "+ str(fprate))
    print("SVM F1: "+ str(svm_f1))
    print("SVM Precision: "+ str(svm_precision))
    print("SVM Recall: "+ str(svm_recall))
    print("SVM tn, fp, fn, tp: "+ str([tn, fp, fn, tp]))
    if print_out:
        print("SVM Accuracy Score -> ",svm_accuracy)

    Log.log("SVM model trained with accuarcy : "+str(svm_accuracy), "train.py")
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
    nb_accuarcy=accuracy_score(test_y, predictions_NB)*100
    nb_precision=precision_score(test_y, predictions_NB)*100
    nb_recall=recall_score(test_y, predictions_NB)*100
    nb_f1= f1_score(test_y, predictions_NB, average=None )
    tn, fp, fn, tp = confusion_matrix(test_y, predictions_NB).ravel()
    fscore = (2*(nb_precision*nb_recall)/(nb_precision+nb_recall))
    fnrate = (fn /len(test_y)) *100
    fprate = (fp /len(test_y)) *100
    print("f-score : "+str(fscore))
    print("fn rate : "+str(fnrate))
    print("fp rate : "+ str(fprate))
    print("SVM F1: "+ str(nb_f1))
    print("SVM Precision: "+ str(nb_precision))
    print("SVM Recall: "+ str(nb_recall))
    print("SVM tn, fp, fn, tp: "+ str([tn, fp, fn, tp]))
    if print_out:
        print("Naive Bayes Accuracy Score -> ",nb_accuarcy)
    
    Log.log("Naive Bayes model trained with accuarcy : "+str(nb_accuarcy), "train.py")
    # Save NB to file in the current working directory
    if save_model:
        with open(join(d,"trained_models","naive_bayes_model.pkl"), 'wb') as filenaive:
            pickle.dump(Naive, filenaive)
        Log.log("NB Model Saved to trained_models\\naive_bayes_model.pkl", "train.py")
    else:
        Log.warning("NB Model Not Saved, save_model parameter not setted true. unable use pretrained model in feature.", "train.py")
    
    return nb_accuarcy

def fit_knn(train_x , train_y, test_x, test_y, save_model=True,print_out=True):
    #NAIVE BAYES:
    #fitting dataset for NB Classifier
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(train_x,train_y)
    #Test : Predict for validation
    predictions_knn = knn.predict(test_x)
    #Use accuracy_score function to get the accuracy
    knn_accuarcy=accuracy_score(test_y, predictions_knn)*100
    knn_precision=precision_score(test_y, predictions_knn)*100
    knn_recall=recall_score(test_y, predictions_knn)*100
    knn_f1= f1_score(test_y, predictions_knn, average=None )
    tn, fp, fn, tp = confusion_matrix(test_y, predictions_knn).ravel()
    fscore = (2*(knn_precision*knn_recall)/(knn_precision+knn_recall))
    fnrate = (fn /len(test_y)) *100
    fprate = (fp /len(test_y)) *100
    print("f-score : "+str(fscore))
    print("fn rate : "+str(fnrate))
    print("fp rate : "+ str(fprate))
    print("knn F1: "+ str(knn_f1))
    print("knn Precision: "+ str(knn_precision))
    print("knn Recall: "+ str(knn_recall))
    print("knn tn, fp, fn, tp: "+ str([tn, fp, fn, tp]))
    if print_out:
        print("knn Accuracy Score -> ",knn_accuarcy)
    
    Log.log("knn model trained with accuarcy : "+str(knn_accuarcy), "train.py")
    # Save NB to file in the current working directory
    if save_model:
        with open(join(d,"trained_models","knn_model.pkl"), 'wb') as filenaive:
            pickle.dump(knn, filenaive)
        Log.log("knn Model Saved to trained_models\\knn_model.pkl", "train.py")
    else:
        Log.warning("knn Model Not Saved, save_model parameter not setted true. unable use pretrained model in feature.", "train.py")
    
    return knn_accuarcy