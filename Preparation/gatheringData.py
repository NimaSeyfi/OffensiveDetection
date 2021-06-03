import regex as re
import csv
import time
from googleSearch import search_it
import numpy as np
from os.path import dirname, abspath ,join

d = dirname(dirname(abspath(__file__))) #set files directory path

import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log



def create_splitted_file(queries_file="SearchQueries_Processed.txt", splitted_file='preprocessed_data_splitted.csv',
                        range_start=0,
                        range_end=10,
                        google_search='y',
                        write_columns=True,
                        file_write_type='a'):
    f = open(join(d,"files\SearchQueries\processed",queries_file), "r",encoding='utf8')
    queries_list_last =f.read().splitlines()
    queries_list_last = list(dict.fromkeys(queries_list_last))
    f.close()
    #create splitted text csv file:
    with open(join(d,"files",splitted_file), file_write_type, encoding='utf-8',newline='') as csvFile:
        writer = csv.writer(csvFile)
        if write_columns and range_start==0:
            writer.writerows([['query', 'titles','links','descs']])
        if range_end==-1:
            range_finish = len(queries_list_last)
        elif range_end<=len(queries_list_last):
            range_finish = range_end
        else:
            range_finish = len(queries_list_last)

        for i in range(range_start,range_finish):
            query=queries_list_last[i]
            print(i)  
            #dont use google
            if google_search=='n':
                links_string=""
                descripstions_string=""
                titles_string=""
                writer.writerows([[str(query),str(titles_string),str(links_string),str(descripstions_string)]])
                csvFile.flush()          
                

            #get google results for query
            else:
                search_results = search_it(query)
                while(search_results==None):
                    search_results = search_it(query)
                links_string=""
                descripstions_string=""
                titles_string=""
                if search_results!=None:
                    for item in search_results:
                        splitted=item.text.splitlines()
                        if(len(splitted)>=3):
                            titles_string=titles_string+splitted[0]+"\r" #one title in each line
                            links_string=links_string+splitted[1]+"\r" #one link in each line
                            #filter results and delete unwanted parts
                            # if("Translate this page" in splitted[2]):
                            #     splitted[2]= splitted[2].replace("Translate this page", '')
                            # if("Rating: " in splitted[2]):
                            #     splitted[2]= ''
                            if(len(splitted)>=4):      
                                descripstions_string=descripstions_string+splitted[3]+"\r" #one description in each line
                            elif(len(splitted)==3):
                                descripstions_string=descripstions_string+splitted[2]+"\r" #one description in each line
                            else:
                                descripstions_string="\r" 
                    writer.writerows([[str(query),str(titles_string),str(links_string),str(descripstions_string)]])
                    csvFile.flush()


            time.sleep(np.random.randint(4,10))
        # logging:
        if google_search=='n':
            Log.log(str(range_finish-range_start)+" data saved correctly to : "+splitted_file,"gatheringData.py")
        elif google_search=='y':
            Log.log(str(range_finish-range_start)+" data saved correctly (google search included) to : "+splitted_file,"gatheringData.py")
        else:
            Log.log(str(range_finish-range_start)+" data saved correctly (google search included) to : "+splitted_file,"gatheringData.py")
            Log.warning("Google search not selected Correctly, using default","gatheringData.py")
    csvFile.close()

'''

askForSearch = input("Search google for the queries?(y/n) : ")
if askForSearch=='n':
    print("Ok! we don't use google search.")
else:
    print("Ok! we use google search.")
print("starting...")

create_splitted_file(google_search=askForSearch)
'''


