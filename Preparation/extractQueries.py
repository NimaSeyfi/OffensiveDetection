import regex as re
import csv
import numpy as np
from os.path import dirname, abspath ,join
d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log

queries_list = []

def query_extratct(line):
    rgx_match='([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+([0-9]+\-[0-9]+\-[0-9]+)\s+([0-9]+\:[0-9]+\:[0-9]+\.[0-9]+)\s+' #regex for deleting ip and dates.
    rgx_match2='\s+[^\s]+\.[^\s]+\s+(http|https).+' #regex for deleting addresses and hash codes.
    line = re.sub(rgx_match, '', line)
    line = re.sub(rgx_match2, '', line)
    return line

def query_extratct2(line):
    rgx_match='([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+([0-9]+\-[0-9]+\-[0-9]+)\s+([0-9]+\:[0-9]+\:[0-9]+\.[0-9]+)\s+' #regex for deleting ip and dates.
    rgx_match2='\s+(Mozilla|UCWEB|MT6735|null|Dalvik|SonyEricsson|SAMSUNG-|python-requests/|Opera|ICC-Crawler|GT-).+' #regex for deleting addresses and hash codes.
    line = re.sub(rgx_match, '', line)
    line = re.sub(rgx_match2, '', line)
    return line

'''
###########################################################################
#                ----------Extracting Queries:------------                #
###########################################################################

#extracting from SearchQueries file and exporting to SearchQueries_Processed file
'''

def extract(src_file ="SearchQueries.txt" , dest_file = "SearchQueries_Processed.txt", mode=1, queries_count = -1):
    queries_list = []
    #extracting from SearchQueries2.txt and exporting to SearchQueries2_Processed.txt
    f = open(join(d,"files\SearchQueries",src_file), "r",encoding='utf8')
    fout=open(join(d,"files\SearchQueries\Processed", dest_file), 'w', encoding='utf8')
    if queries_count==-1: #all queries
        c = file_len(f)
        f = open(join(d,"files\SearchQueries",src_file), "r",encoding='utf8')
    else:
        c = queries_count
    if (mode==1):
        for i in range(c):
            if (mode==1):
                ex_query=query_extratct(f.readline())
            else:
                ex_query=query_extratct2(f.readline())
            if(ex_query not in queries_list and len(ex_query)<150):
                
                fout.write(ex_query)
                fout.flush()
                queries_list.append(ex_query)  
    f.close()
    fout.close()
    Log.log(str(c)+" queries extracted from : "+src_file, "extractQueries.py")



def file_len(f):
    for i, l in enumerate(f):
        pass
    return i + 1


#extract()