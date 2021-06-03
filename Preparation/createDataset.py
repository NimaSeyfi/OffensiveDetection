import csv
import regex as re
from better_profanity import profanity
import tagger
import dictTagger
from os.path import dirname, abspath ,join
import time

d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log

def normalize_url(line): #delete https://www parts of a url (or like this) and split words in url
    rgx_match1='(http:\/\/www.|https:\/\/www.|http:\/\/|https:\/\/|www.)'
    rgx_match2='\s+'
    line = re.sub(rgx_match1, '', line)
    split_chars={'.','-','_',')','(',' ›',' › '} #split words in url by this Chars
    for spl_char in split_chars:
        line=line.replace(spl_char," ")
    line = re.sub(rgx_match2, ' ', line)        
    return line


def create_data_set(splitted_file='preprocessed_data_splitted.csv', dataset_file='preprocessed_data_set.csv', 
                    column_title=False,
                    start_data_number=0,
                    tagger_strictness=12,
                    forced_value=False,
                    value_forced=1):
    csvDataset=open(join(d,"files",dataset_file), 'a', encoding='utf-8',newline='') #dataset file
    writer = csv.writer(csvDataset)

    if column_title:
        writer.writerows([['text','label']])
        Log.log("colummns title writed in first line" , "createDataset.py")
    #Create dataset file from splitted file:
    #out put is a csv File with 2 columns : Text , Label
    #Label is getting from a persian API based NLP Tool by text-minig.ir , and also a Enlish words Swear words detector "better-porfanity"
    with open(join(d,"files",splitted_file), 'r', encoding='utf-8',newline='') as csvFileSplitted:
        csv_reader = csv.reader(csvFileSplitted, delimiter=',')
        line_count = 0
        counter=0
        for row in csv_reader:
            counter+=1
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif counter>start_data_number:
                print(counter)
                
                links=row[2].splitlines()
                links_str=' '.join([normalize_url(line) for line in links]) #normalize links
                text_str=row[0]+" "+row[1].replace("\r"," ")+links_str+row[3].replace("\r"," ") #Extract a normalized text from splitted csv file
                #labeling
                if forced_value:
                    writer.writerows([[str(text_str), str(value_forced)]])
                    csvDataset.flush()  
                else:
                    if tagger.SwearWordTagger(text_str,strictness=tagger_strictness) or profanity.contains_profanity(text_str) or  dictTagger.dictionary_tagger(text_str):
                        #print('OFFENSIVE')
                        writer.writerows([[str(text_str), '1']]) #1 is offensive
                        csvDataset.flush()  
                    else:
                        #print('NOT-OFFENSIVE')
                        writer.writerows([[str(text_str), '0']]) #0 is non-offensive
                        csvDataset.flush()
                time.sleep(2)  
            
        Log.log("dataset text and lable processed and saved to : "+dataset_file , "createDataset.py")            
        csvFileSplitted.close()            
        csvDataset.close()

def create_input_text(splitted_file='preprocessed_data_splitted.csv', dataset_file='preprocessed_data_set.csv', 
                    column_title=False,
                    start_data_number=0):
    csvDataset=open(join(d,"files",dataset_file), 'w', encoding='utf-8',newline='') #dataset file
    writer = csv.writer(csvDataset)

    if column_title:
        writer.writerows([['text']])
        Log.log("colummns title writed in first line" , "createDataset.py")
    #Create dataset file from splitted file:
    #out put is a csv File with 2 columns : Text , Label
    #Label is getting from a persian API based NLP Tool by text-minig.ir , and also a Enlish words Swear words detector "better-porfanity"
    with open(join(d,"files",splitted_file), 'r', encoding='utf-8',newline='') as csvFileSplitted:
        csv_reader = csv.reader(csvFileSplitted, delimiter=',')
        line_count = 0
        counter=0
        for row in csv_reader:
            counter+=1
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif counter>start_data_number:
                #print(counter)
                
                links=row[2].splitlines()
                links_str=' '.join([normalize_url(line) for line in links]) #normalize links
                text_str=row[0]+" "+row[1].replace("\r"," ")+links_str+row[3].replace("\r"," ") #Extract a normalized text from splitted csv file
                writer.writerows([[str(text_str)]])
                csvDataset.flush()  

        Log.log("input text processed and saved to : "+dataset_file , "createDataset.py")            
        csvFileSplitted.close()            
        csvDataset.close()