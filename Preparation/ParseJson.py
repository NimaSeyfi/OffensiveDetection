import json
from os.path import dirname, abspath ,join
d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)

swear_farsi = []

with open(join(d,"files",'farsi-swears.txt'), 'a', encoding='utf-8',newline='') as swears:
    json_file = open(join(d,"files",'Persian-Swear-Words.json'), 'r', encoding='utf-8',newline='')
    data = json.load(json_file)
    for p in data['word']:
        # swears.write(p+"\n")
        swear_farsi.append(p)
    
    for i in range(len(swear_farsi)):
        swear_farsi.append(swear_farsi[i] + ' ' + swear_farsi[(i + 10) % len(swear_farsi)])
    
    for p in swear_farsi:
        swears.write(p+"\n")
