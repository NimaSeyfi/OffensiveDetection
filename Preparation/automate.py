import time
import numpy as np
from gatheringData import create_splitted_file


def automate(sleep=500,start=0,end=1000,interval=100):
    new_start=start
    if new_start+interval <= end:
        new_end=new_start+interval
    else:
        new_end=end
    for i in range(0,(end-start)//interval):
        
        create_splitted_file(queries_file="SearchQueries_all_extracted.txt", splitted_file='Dataset_Splitted_datas.csv',
                            range_start=new_start,
                            range_end=new_end,
                            google_search='y',
                            write_columns=False,
                            file_write_type='a')


        timer=np.random.randint(sleep-30,sleep+30)
        print("sleep for "+str(timer) + " seconds.")
        
        time.sleep(timer)

        new_start=new_end+1
        if new_start+interval-1 <= end:
            new_end=new_start+interval-1
        else:
            new_end=end


automate(500,6400,7400)