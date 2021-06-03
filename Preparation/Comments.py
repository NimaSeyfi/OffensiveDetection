import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.by import By
import pyodbc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import regex as re
import csv
import numpy as np
import demoji
from os.path import dirname, abspath ,join

d = dirname(dirname(abspath(__file__))) #set files directory path

import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log





def insta_login(redirect_url, driver = webdriver,username = "nimatestinsta", password = "nima1234"):
        
        driver.get(redirect_url)
        time.sleep(10)
        try:
                dialog = driver.find_element_by_xpath("//div[@role = 'dialog']")
                dialog.find_element_by_class_name('bIiDR').click()
                time.sleep(10)
        except:
                time.sleep(10)
                pass
        driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
        time.sleep(10)
        if 'onetap' in driver.current_url:
                driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
        
        time.sleep(20)


def get_post_cms(driver = webdriver, post_url='https://www.instagram.com/p/CLg4PKaLlK1/', view_more=5, user_name='donya'):
        # post_url=input('Enter Post URL: ')
        # user_name=input('Enter User Name: ')
        
        driver.get(post_url)
        start = time. time()
        time.sleep(25)
        for i in range(0,view_more):
                print("\t - - - view more "+ str(i) + " from "+ str(view_more))
                sl=driver.find_elements_by_link_text(user_name)
                sl[1].get_attribute('title')
                sl[1].send_keys(Keys.END)
                randSleep = random.randint(4,12)
                print('\t - - - - > view more wait for : '+str(randSleep)+' seconds...')
                time.sleep(randSleep)

                try:
                        wait = WebDriverWait(driver, 30)
                        #loadmore_button=wait.until(ec.element_to_be_clickable((By.XPATH,'//button[text()="Load more comments"]')))
                        loadmore_button=wait.until(ec.element_to_be_clickable((By.XPATH,'//span[@aria-label="Load more comments"]')))
                        
                        # time.sleep(randSleep)
                        
                        loadmore_button.click()
                except:
                        try:
                                loadmore_button = driver.find_element_by_xpath("//button[contains(text(), 'View all ')]")
                                loadmore_button.click()
                                sl[1].send_keys(Keys.HOME)
                                break

                        except:
                                break

        end = time. time()
        print('The Process Terminates In',end - start, 'Seconds.')
        return driver.find_elements_by_class_name('gElp9')



def write_cms_csv(comment, driver= webdriver,  comments_file='comments.csv', file_write_type = 'a', write_columns = True, 
        filter_cms = True):
        print("\t - - - - - - "+str(len(comment)) + " recieved from post")
        if filter_cms:
                names_list = read_names_csv()

        start = time. time()
        with open(join(d,"files",comments_file), file_write_type, encoding='utf-8',newline='') as csvFile:
                writer = csv.writer(csvFile)
                if write_columns:
                        writer.writerows([['name', 'comment']])
                for c in comment:
                        try:
                                container = c.find_element_by_class_name('C4VMK')
                                name = container.find_element_by_class_name('_6lAjh').text
                                # content = container.find_element_by_tag_name('span').text
                                #content = content.replace('\n', ' ').strip().rstrip()
                                content = container.text.split('\n')[1]
                                if filter_cms:
                                   content = remove_persian_names(names_list, content)  
                                   content = re.sub(r'(@|https?)\S+|#', '', content) 
                                   content = demoji.replace(content, "")
                                if content != '':   
                                        writer.writerows([[name, content]])
                                        csvFile.flush() 
                        except:
                                pass
        # driver.quit()
        csvFile.close()
        end = time. time()
        print('The Process Terminates In',end - start, 'Seconds.')


def read_names_csv(names_file="persian_names.csv"):
        names_list = []
        with open(join(d,"files",names_file), 'r', encoding='utf-8',newline='') as namesCsv:
                csv_reader = csv.reader(namesCsv, delimiter=',')
                line_count = 0
                counter=0
                for row in csv_reader:
                        names_list.append(row[1])        
                namesCsv.close()   
        return names_list

def remove_persian_names(names, comment):
        for name in names:
                if name in comment:
                        comment = comment.replace(name , "")
        
        return comment





chromedriver = './chromedriver.exe'
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# options.set_headless(True)
webdriver = webdriver.Chrome( options=options)


post_list = ['https://www.instagram.com/p/CLg4PKaLlK1/', 'https://www.instagram.com/p/CLAJLqglkWe/',
                'https://www.instagram.com/p/CL37OmBrn1m/','https://www.instagram.com/p/CE8otyoAddq/',
                'https://www.instagram.com/p/CBLmIFMg2Go/','https://www.instagram.com/p/CL4uJvPDCvW/',
                'https://www.instagram.com/p/CLgwMSWDenr/','https://www.instagram.com/p/CL-OVqRBxH3/',
                'https://www.instagram.com/p/CL9rFKnAHQu/']
username_list = ['donya', 'elnaz_golrokh', 'perspolis','sadaftaheriann','sadaftaheriann','i.wonders'
                ,'i.wonders', 'iranintltv'
                ]
# write_cms_csv(get_post_cms(webdriver,post_list[0], random.randint(30,100),username_list[0]),
                #  webdriver)
# print("post 0 from "+ str(len(post_list))+" done. sleep for 11 min.")
# time.sleep(650)
insta_login(post_list[0], webdriver)
for i in range(6,len(post_list)):
        write_cms_csv(get_post_cms(webdriver,post_list[i], random.randint(200,500),username_list[i]),
                 webdriver,write_columns=False)
        rand = random.randint(650,1000)
        print("post "+str(i)+" from "+ str(len(post_list))+" done. sleep for " + str(rand)+ " sec.")
        time.sleep(rand)

driver.quit()

        

