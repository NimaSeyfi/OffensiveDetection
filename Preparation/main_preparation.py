from extractQueries import extract
from gatheringData import create_splitted_file
from createDataset import create_data_set
from os.path import dirname, abspath ,join
d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log

# ifExtract = input("Extract the queries?(y/n) : ")
# if ifExtract=='n':
#     print("Ok! we don't extract queries")
# else:
#     src_queries = input("-Enter queries source : ")   
#     print("--use queries from file : "+src_queries)

#     dest_queries = input("-Enter queries destination : ")   
#     print("--save queries to file : "+dest_queries)

#     queries_count = input("-Enter queries count to extract : ")   
#     print("--queries count : "+queries_count)

#     extract_mode = input("-Enter queries mode : (1/2) ")   
#     print("--extract queries mode : "+extract_mode)

#     Log.log("Extract "+queries_count+" queries from "+ src_queries +" to "+dest_queries + " - mode : "+extract_mode,"mainPreprocess.py")

# ifCreateSplitted = input("Create data and split it (y/n) : ")
# if ifCreateSplitted=='n':
#     print("Ok! we don't create Splitted dataset")
# else:
#     if ifExtract=='n':
#         dest_queries = input("-Enter queries source : ")   
#         print("--use queries from file : "+dest_queries)

#     splitted_file_path = input("-Enter splitted data file destination : ")   
#     print("--save splitted file to : "+splitted_file_path)

#     range_s = input("-Enter queries start range to generate data : ")   
#     print("--start range : "+range_s)

#     range_e = input("-Enter queries end range to generate data : ")   
#     print("--end range : "+range_e)

#     askForSearch = input("Search google for the queries?(y/n) : ")
#     if askForSearch=='n':
#         print("Ok! we don't use google search.")
#     else:
#         print("Ok! we use google search.")

#     Log.log("Get data and create splitted dataset from "+dest_queries+" to "+splitted_file_path+" range "+range_s+" to "+range_e
#     + " (google search : "+askForSearch+")" ,"mainPreprocess.py")

# ifCreateDataset = input("Create dataset and lable datas (y/n) : ")
# if ifCreateDataset=='n':
#     print("Ok! we don't extract dataset.")
# else:
#     if ifCreateSplitted=='n':
#         splitted_file_path = input("-Enter splitted data file name : ")   
#         print("--get splitted datas from : "+splitted_file_path)

#     dataset_file_path = input("-Enter dataset file name : ")   
#     print("--save dataset to file : "+dataset_file_path)

#     column_title_on = input("-Write titles on dataset (for first time) : ")   

#     start_write_data_number = input("-write datas after how many rows : ")   
#     print("--start write from : "+start_write_data_number)

#     tag_strictness = input("-tagger stricness (enter 12 for default value) : ")

#     Log.log("create dataset from "+splitted_file_path+" to "+dataset_file_path+" -columns : "+column_title_on+" -start write data : "+
#     start_write_data_number+" - Tagger Strictness : "+tag_strictness ,"mainPreprocess.py")


# print("starting...")


# if ifExtract=='y':
#     extract(src_file =src_queries , dest_file =dest_queries, mode=int(extract_mode), queries_count = int(queries_count))

# if ifCreateSplitted=='y':
#     create_splitted_file(queries_file=dest_queries, splitted_file=splitted_file_path,
#                             range_start=int(range_s),
#                             range_end=int(range_e),
#                             google_search=askForSearch)

# if ifCreateDataset=='y':
#     create_data_set(splitted_file=splitted_file_path, dataset_file=dataset_file_path, 
#                         column_title=column_title_on,
#                         start_data_number=int(start_write_data_number),
#                         tagger_strictness=int(tag_strictness)
#                         )

create_splitted_file(queries_file='OffensiveQ.txt', splitted_file='OffSplitted.csv',
                            range_start=0,
                            range_end=-1,
                            google_search='y')

create_data_set(splitted_file='OffSplitted.csv', dataset_file='OffDataset.csv', 
                        column_title='n',
                        forced_value=True
                        )