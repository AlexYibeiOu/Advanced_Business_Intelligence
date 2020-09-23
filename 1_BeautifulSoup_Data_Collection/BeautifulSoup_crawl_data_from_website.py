# This program uses BeautifulSoup to crawl data from an Auto safety accident website and then
# save data to a csv file.

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Set URL
url  = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml'

# Get page content
headers={'user-agent':'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.131 Safari/537.36'}
html=requests.get(url,headers=headers,timeout=10)
content=html.text
# create an BeautifulSoup object by content
soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

print(soup.title)
print(soup.title.name)
print(soup.title.string)

# Get soup from URL
def get_page_content(request_url):
    headers={'user-agent':'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content=html.text
    # create an BeautifulSoup object by content
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# anaylysis soup
def analysis(soup):
    temp = soup.find('div', class_='tslb_b')

    df = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    # get all rows in table
    tr_list=temp.find_all('tr')

    for tr in tr_list:
        temp = {}
        # get all 
        td_list = tr.find_all('td')

        if len(td_list) > 0:
            id, brand, car_model, type, desc, problem, datetime, status = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            temp['id'] = id    
            temp['brand'] = brand
            temp['car_model'] = car_model
            temp['type'] = type
            temp['desc'] = desc
            temp['problem'] = problem
            temp['datetime'] = datetime
            temp['status'] = status
            df = df.append(temp, ignore_index=True)
    return df

# result is full datasets
result = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
page_name = 4
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'

# Start crawling
for i in range(page_name):
    # 
    request_url = base_url + str(i+1) + '.shtml'
    print(request_url)
    # get soup from url
    soup = get_page_content(request_url)
    df = analysis(soup)
    print(df)
    result = result.append(df)

# Save to file
result.to_csv('car3.csv', index=False)