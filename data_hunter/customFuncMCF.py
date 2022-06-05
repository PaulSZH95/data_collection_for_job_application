import sys
import pandas as pd
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
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

###############functions######################################################

start_time = time.time()

def even_num_gen(a,b):
    return list(range(a,b,2))


def data_to_table(driver,newurl):
    driver.get(newurl)
    # use explicit wait for loading of pages with urls
    wait = WebDriverWait(driver, 100)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for=non_executive]'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for=junior_executive]'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for=fresh_entry_level]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results"]/div[7]/span[4]')))


    # force wait for at least 5 seconds because the dom tree html is lagging and i cant find tags to use to implicit or explicit wait
    time.sleep(10)
    ncontent = driver.page_source
    soup = bs(ncontent, 'html.parser')
    # with open('ht.txt', mode='wt', encoding='utf-8') as ht:
    #     for i in soup.contents:
    #         ht.write(str(i))
    org_url = 'https://www.mycareersfuture.gov.sg'

    #changes to last-commit: as find_all appears to give duplicates and sometimes there may be different number of results, we will use len(find_all) instead of static number

    hyperlinks = [org_url + i['href'] for i in soup.find_all('a', {'data-testid':"job-card-link"})]

    applicants = [[i.get_text() for i in soup.find_all('span', {'data-cy':"job-card__num-of-applications"})][j] for j in even_num_gen(0,len(soup.find_all('span', {'data-cy':"job-card__num-of-applications"})))]

    company_name = [i.get_text() for i in soup.find_all('p', {'data-cy':"company-hire-info__company"})]

    posted_days_ago = [[i.get_text() for i in soup.find_all('span', {'data-cy':"job-card-date-info"})][j] for j in even_num_gen(0,len(soup.find_all('span', {'data-cy':"job-card-date-info"})))]

    industry = [[i.get_text() for i in soup.find_all('p', {'data-cy':"job-card__category"})][j] for j in even_num_gen(0,len(soup.find_all('p', {'data-cy':"job-card__category"})))]

### webstite changed their html, refactored for the updates. 
    pay = {}
    for i in soup.find_all('span',{"data-cy":"salary-range"}):
        pay['max_pay'] = pay.get('max_pay', [])
        pay['min_pay'] = pay.get('min_pay', [])
        pay['max_pay'].append([j.get_text() for j in i.find_all('span', {"class":"dib"})][0])
        pay['min_pay'].append([j.get_text()[2:] for j in i.find_all('span', {"class":"dib"})][1])

    
    return {'hyperlinks':hyperlinks,'applicants':applicants,'company_name':company_name,'posted_days_ago,industry':posted_days_ago,'industry':industry,'max_pay':pay['max_pay'],'min_pay':pay['min_pay']}


def give_me_text(list1,list2):
    compress_list1 = [c[b] for c in [a.find_all('li') for a in list1] for b in range(len(c)) ]
    compress_list2 = [c[b] for c in [a.find_all('li') for a in list2] for b in range(len(c)) ]
    text_1 = '\n'.join([i.get_text() for i in compress_list1])
    text_2 = '\n'.join([i.get_text() for i in compress_list2])

    return text_1,text_2

def ordering(ncontent):
    soup = bs(ncontent, 'html.parser')
    header = soup.find('div', {'class':"jobDescription"})
    content = header.find_all('ul')
    if len(content) > 2:
        list1 = content[:2]
        list2 = content[2:]
        return give_me_text(list1,list2)
    elif len(content) == 2:
        try:
            list1 = [content[0]]
        except Exception as er:
            print(content)
            print(er)
        try:
            list2 = [content[1]]
        except Exception as er:
            print(content)
            print(er)
        return give_me_text(list1,list2)
    elif len(content) == 2:
        try:
            return give_me_text(content,content)
        except Exception as er:
            print(content)
            print(er)
    else:
        try:
            content2=soup.find_all('div',{'id':"description-content"})
            list1 = ['']
            list2 = [''] 
            for i in content2:
                if i.name != 'h1':
                    list1.append(i.get_text())
                else:
                    list2.append(i.get_text())
            text_1 = '\n'.join(list1)
            text_2 = '\n'.join(list2)
            return text_1,text_2
        except:
            return 'no result','no result'


################ make our driver ####################################################################
def browser_sim(url,searches,driver_loc,dir):

    options = wd.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # hide stupid error, mostly from insecure certs
    options.add_argument("--headless") #make it headless
    options.add_argument("--window-size=1440, 900") #give max size of browser
    #driver.maximize_window() # this optopn will overcome overlapping of elements
    driver = wd.Chrome(executable_path = driver_loc,options=options)
    #I want to make driver wait for at least 5 sec to find any element
    driver.implicitly_wait(5) 
    driver.get(url)

    ############# driver created above ############################################################################

    driver.find_element_by_class_name("react-autosuggest__input").send_keys(searches)
    # using actionchain for js loaded websites
    action = ActionChains(driver)
    node1 = driver.find_element_by_id("react-select-2--value-item")
    action.move_to_element(node1).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
    driver.find_element_by_id("search-button").click()



    dict_of_job = {}

    for i in range(2):
        currenturl = driver.current_url
        newurl = currenturl[:-1] + str(i)
        data = data_to_table(driver,newurl)
        for i in data:
            dict_of_job[i] = dict_of_job.get(i,[])
            dict_of_job[i] = dict_of_job[i] + data[str(i)]
    df = pd.DataFrame(dict_of_job)
    df.to_csv(f'{dir}url_data_{datetime.date.today()}{searches}.csv',index=False)

    ### added strip to remove white space
    dict_of_job['desc'] = []
    dict_of_job['req'] = []
    for url in df['hyperlinks']:
        driver.get(url)
        time.sleep(3)
        ncontent = driver.page_source
        try:
            text_1,text_2 = ordering(ncontent)
            dict_of_job['desc'].append(text_1.strip())
            dict_of_job['req'].append(text_2.strip())
        except Exception as er:
            print('hyperlinks')
            dict_of_job['desc'].append('')
            dict_of_job['req'].append('')
            print(er)
        

    df1 = pd.DataFrame(dict_of_job)

    #print(df1)
    df1.to_csv(f'{dir}url_desc_{datetime.date.today()}{searches}.csv',index=False)

    print(time.time() - start_time)