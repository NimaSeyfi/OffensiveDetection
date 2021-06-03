from os.path import dirname, abspath ,join
d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log
from Preparation.gatheringData import create_splitted_file
from Preparation.createDataset import create_input_text

input_queries_file = "input_queries.txt"
input_queries_splitted_file = "input_queries_splitted.csv"
input_queries_dataset_file = "input_queries_dataset.csv"


def input_preprocess():
    create_splitted_file(queries_file=input_queries_file, splitted_file=input_queries_splitted_file,
                            range_start=0,
                            range_end=-1,
                            google_search='y',
                            write_columns=True,
                            file_write_type='w'
                            )

    create_input_text(splitted_file=input_queries_splitted_file, dataset_file=input_queries_dataset_file, 
                            column_title=True,
                            start_data_number=0
                            )