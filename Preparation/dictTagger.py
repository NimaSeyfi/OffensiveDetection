from os.path import dirname, abspath ,join

d = dirname(dirname(abspath(__file__))) #set files directory path

dictionary_file=open(join(d,"files",'offensive_dictionary.txt'), 'r', encoding='utf-8',newline='') #dictionary file
offensive_counter=1

def dictionary_tagger(input_str):
    temp_counter=0
    for line in dictionary_file:
        y = line.split('\r')
        if y[0] in input_str:                                  
            temp_counter=temp_counter+1
            if offensive_counter==temp_counter:
                print("offensive from dictionary")  
                return True
                break
    return False        
