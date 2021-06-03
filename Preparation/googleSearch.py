from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
from os.path import dirname, abspath ,join

d = dirname(dirname(abspath(__file__))) #set files directory path
import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, d)
import Log

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(join(d,'chromedriver.exe'), options=options)
RESULTS_LOCATOR = "tF2Cxc"


def search_it(query):
    try:
        driver.get("http://www.google.com")
        time.sleep(4.5)
        input_element = driver.find_element_by_xpath("//input[@name='q']")
        input_element.send_keys(query)
        input_element.submit()
        page1_results = driver.find_elements_by_class_name(RESULTS_LOCATOR)
        #for item in page1_results:
        #   print(item.text.splitlines()) 
        return page1_results
    except:
        Log.error("Google search-error catched-query : {"+query[0:30]+"}","googleSearch.py")
        print("-error catched")
        return None
    