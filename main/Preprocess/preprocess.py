from __future__ import unicode_literals
import pickle
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords as stpwrd
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn import model_selection
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from PersianStemmer import PersianStemmer 
from hazm import *
from os.path import dirname, abspath ,join
import pickle
import random

d = dirname(dirname(dirname(abspath(__file__)))) #set files directory path



    
#print(Test_X_Tfidf.shape)
#print(Tfidf_vect.vocabulary_)

#adding persian stopwords to nltk stopwords list:
stopwords = stpwrd.words('english')
persian = open(join(d,"stopwordlists","persian"),encoding="utf-8").read().splitlines()
nonverbal = open(join(d,"stopwordlists","nonverbal"),encoding="utf-8").read().splitlines()
short = open(join(d,"stopwordlists","short"),encoding="utf-8").read().splitlines()
verbal = open(join(d,"stopwordlists","verbal"),encoding="utf-8").read().splitlines()
chars = open(join(d,"stopwordlists","chars"),encoding="utf-8").read().splitlines()
stopwords.extend(persian)
stopwords.extend(nonverbal)
stopwords.extend(short)
stopwords.extend(verbal)
stopwords.extend(chars)
    


ps = PersianStemmer()
np.random.seed(500)



def preprocess(dataset="preprocessed_data_set.csv", test_data_percent=0.25):
    '''
    ####################################################################
    #########################PREPROCESS SECTION#########################
    ####################################################################
    '''
    #Step by Step Tasks to prepare dataset for learning:

    #Reading the dataset
    Corpus = pd.read_csv(join(d,"files",dataset),encoding='utf-8')
    #Remove blank rows if any.
    Corpus['text'].dropna(inplace=True)
    #Change all the text to lower case.
    Corpus['text'] = [entry.lower() for entry in Corpus['text']]
    #Normalize persian sentences
    normalizer = Normalizer()
    Corpus['text'] = [normalizer.normalize(entry) for entry in Corpus['text']]
    #for entry in Corpus['text']:
    #    print(entry)

    #Tokenization : In this each entry in the corpus will be broken into set of words
    Corpus['text']= [word_tokenize(entry) for entry in Corpus['text']]
    #Remove Stop words, Non-Numeric and perfom Word Stemming/Lemmenting.
    #Persian words Stemming
    for entry in Corpus['text']:
        for token in entry:
            token=ps.run(token)
    #WordNetLemmatizer tagging
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    for index,entry in enumerate(Corpus['text']):
        Final_words = [] #output list
        #Enlgish words lemmenting
        word_Lemmatized = WordNetLemmatizer()    # Initializing WordNetLemmatizer()
        #pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
        for word, tag in pos_tag(entry):
            #check for Stop words and consider only alphabets
            if word not in stopwords and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                Final_words.append(word_Final)
        #The final processed set of words for each iteration will be stored in 'text_final'
        Corpus.loc[index,'text_final'] = str(Final_words)
    
    #Prepare train and test set for learning  
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['text_final'],
                                                                        Corpus['label'],test_size=test_data_percent)

    #encoding labels to numbers
    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Train_Y)
    Test_Y = Encoder.fit_transform(Test_Y)

    #Apply TFIDF method for vectorizing words
    Tfidf_vect = TfidfVectorizer(max_features=10000)
    Tfidf_vect.fit(Corpus['text_final'])
    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X) 
    #save tfidf vectorizer
    with open(join(d,"trained_models","tfidf_vectorizer_vocab.pkl"), 'wb') as filevec:
        pickle.dump(Tfidf_vect.vocabulary_, filevec)

    return Train_X_Tfidf, Train_Y , Test_X_Tfidf , Test_Y


def preprocess_input(input_str,transformer_in,vec_in): 
    #load vectorizer:
    transformer = transformer_in
    loaded_vec = vec_in
    ps = PersianStemmer()  
    #Step by Step Tasks to prepare dataset for learning
    #Reading the dataset
    Corpus = pd.read_csv(join(d,"files",'input_queries_dataset.csv'),encoding='utf-8')
    #Remove blank rows if any.
    Corpus['text'].dropna(inplace=True)
    #Change all the text to lower case.
    Corpus['text'] = [entry.lower() for entry in Corpus['text']]
    #Normalize persian sentences
    normalizer = Normalizer()
    Corpus['text'] = [normalizer.normalize(entry) for entry in Corpus['text']]
    
    #Tokenization : In this each entry in the corpus will be broken into set of words
    Corpus['text']= [word_tokenize(entry) for entry in Corpus['text']]
    #Remove Stop words, Non-Numeric and perfom Word Stemming/Lemmenting.
    #Persian words Stemming
    for entry in Corpus['text']:
        for token in entry:
            token=ps.run(token)
    #WordNetLemmatizer tagging
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    for index,entry in enumerate(Corpus['text']):
        Final_words = [] #output list
        #Enlgish words lemmenting
        word_Lemmatized = WordNetLemmatizer()    # Initializing WordNetLemmatizer()
        #pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
        for word, tag in pos_tag(entry):
            #check for Stop words and consider only alphabets
            if word not in stopwords and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                Final_words.append(word_Final)
        #The final processed set of words for each iteration will be stored in 'text_final'
        Corpus.loc[index,'text_final'] = str(Final_words)
    
    #Prepare train and test set for learning  
    line=Corpus['text_final']   
    #print(line)
    #Apply TFIDF method for vectorizing words
    line_Tfidf = transformer.fit_transform(loaded_vec.fit_transform(line))
    return line_Tfidf

    
    