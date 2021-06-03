import requests
import json
from os.path import dirname, abspath ,join
d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log

def callApi(url, data, tokenKey):
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + tokenKey,
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", url, data=data.encode("utf-8"), headers=headers)
    return response.text

##################### Get Token by Api Key ##########################

baseUrl = "http://api.text-mining.ir/api/"
url = baseUrl + "Token/GetToken"
querystring = {"apikey":"bddb2a1d-ed80-eb11-80ee-98ded002619b"}
response = requests.request("GET", url, params=querystring)
data = json.loads(response.text)
tokenKey = data['token']
################## Call Swear Word Detector ######################
def SwearWordTagger(text, strictness):
    url =  baseUrl + "TextRefinement/SwearWordTagger"
    payload = "\""+text+"\""
    if strictness>=3 : #Strictness should be greater than 3.
        result = json.loads(callApi(url, payload, tokenKey))
        #print(result) #Show result of sent text. comment it if you dont want this 
        if list(result.values()).count('StrongSwearWord')>=int(strictness/3) or list(result.values()).count('StrongSwearWord')+list(result.values()).count('MildSwearWord')>=int(strictness-2) or list(result.values()).count('MildSwearWord')>=int(strictness):
            return True
        else:
            return False
    else:
        Log.error("Strictness should be greater than 3.", "tagger.py")
        return False
            
        
        
        