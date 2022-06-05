import pandas as pd
from regex import F
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import datetime

############################ hide ######################################################

'''
with wd.Chrome(executable_path = driver_loc) as driver:
    driver.get(url)
    connect = driver.find_element_by_class_name("react-autosuggest__input")
    connect.send_keys('ai')
'''
################################################################################################

start_time = time.time()

def get_cont_uni(needle):
    top = []
    for i in needle.children:
        try:
            kl = i.get_text()
            top.append(kl.strip())
        except:
            continue
    return top

################ make our driver ####################################################################
def search_linkedin(searches,location,driver_loc,dir):
    url = f"https://www.linkedin.com/jobs/search?keywords={searches}&location={location}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&f_TPR=r604800&f_JT=F%2CC&f_E=2%2C3&position=1&pageNum=0"
    options = wd.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # hide stupid error, mostly from insecure certs
    options.add_argument("--headless") #make it headless
    options.add_argument("window-size=1920,1080") #give max size of browser
    #driver.maximize_window() # this optopn will overcome overlapping of elements
    driver = wd.Chrome(executable_path = driver_loc,options=options)
    #I want to make driver wait for at least 5 sec to find any element
    driver.implicitly_wait(5) 
    driver.get(url)

    ############# driver created above ############################################################################

    tot_jobs = driver.find_element_by_class_name("results-context-header__job-count").get_attribute("textContent")

    try:
        tot_job = int(tot_jobs)
    except:
        tot_job = re.findall("[0-9]+", tot_jobs)
        tot_job = ''.join(tot_job).strip()
        tot_job = int(tot_job)

    if tot_job > 400:
        tot_job = 400
    if (tot_job/25) == 0 :
        num_range = tot_job/25
    else:
        num_range = round(tot_job/25) + 1

    count = 25
    state = 1
    for i in range(num_range):
        time.sleep(1)
        driver.execute_script(f"window.scrollTo(0,document.body.scrollHeight);")
        clicker = True
        count += 25 
        while clicker:
            try:
                wait = WebDriverWait(driver, 5)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/section[2]/button'))).click()
                count += 25
                state = 0
                if tot_job == 400 and count >= 400:
                    clicker = False
                else:
                    continue
            except:
                clicker = False
                continue
        if state == 0:
            break


    data_dict={}
    time.sleep(10)
    content = driver.find_element(By.CSS_SELECTOR, 'ul.jobs-search__results-list')
    jobtitile= [i.text for i in content.find_elements(By.CSS_SELECTOR, 'h3.base-search-card__title')]
    joblink = [i.find_element_by_tag_name('a').get_attribute('href') for i in content.find_elements(By.TAG_NAME,'li')]
    jobloc=[i.find_element(By.CSS_SELECTOR,'span.job-search-card__location').text for i in content.find_elements(By.TAG_NAME,'li')]
    jobcoy = [i.text for i in content.find_elements(By.CSS_SELECTOR, 'h4.base-search-card__subtitle')]
    #time.sleep(5)
    # jobstatus = [i.text for i in content.find_elements(By.CSS_SELECTOR, 'span.result-benefits__text')]
    # job status sometimes gives error so f it 
    jobpostedate = [i.get_attribute('datetime') for i in content.find_elements(By.CSS_SELECTOR, 'time')]
    driver.close()

    data_dict['Job Title']=jobtitile
    data_dict['Job Link']=joblink
    data_dict['Job Location']=jobloc
    data_dict['Job Company']=jobcoy
    # data_dict['Job Status']=jobstatus
    data_dict['Job Post Date']=jobpostedate

    # lengt = [(i,len(data_dict[i])) for i in data_dict]
    # print(lengt)

    # df = pd.DataFrame(data_dict)
    # df.to_csv(f'{dir}jobs_w_o_desc{datetime.date.today()}{searches}from_linkedin.csv',index=False)


    ##### since the url are static links, we do not need selenium after the dict is made
    # for i in jobtitile:
    # settle for one link then we loop for all link:

    jobdesc = []

    for i in joblink:
        try:
            j = requests.get(i)
            jobd = []
            time.sleep(2)
            soup = bs(j.text, 'html.parser')
            needle = soup.find('section',{"class":"show-more-less-html"})
            k = ''.join(get_cont_uni(needle))
            jobdesc.append(k)
        except:
            jobdesc.append("req timeout")



    data_dict['Job Description']=jobdesc

    # lengt = [(i,len(data_dict[i])) for i in data_dict]

    # print(lengt)

    df = pd.DataFrame(data_dict)
    df.to_csv(f'{dir}jobs{datetime.date.today()}{searches}from_linkedin.csv',index=False)

    print(time.time() - start_time)
    #print(simpli)
    #print(tt)

# # test:
# searches = "ai"
# location = "singapore" # change it to whatever u want
# driver_loc="./chromedriver.exe"  #comment when running as lib
# dir='./'#"./resources/" to be put above
# search_linkedin(searches,location,driver_loc,dir)