import csv
from bs4 import BeautifulSoup
import requests


search_item = "Ubisoft" # <------ ENTER SEARCH ITEM HERE

records = []


def get_url(search_term):
	print("URLs")
	base_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss_2"
	search_term = search_term.replace(' ','+')
	url = base_url.format(search_term)
	url += '&page{}'

	return url

def extract_record(item):
    print("Processing Records")
    #Name and URL
    atag = item.h2.a
    name = atag.text.strip()
    url = "https://www.amazon.in" + atag.get('href')
    
    #Price
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
    
    #Rating and COunt
    try:
        rating = item.i.text
        count_parent = item.find('a',{'class':'a-link-normal'})
        count = count_parent.find('span',{'class':'a-size-base'})
    except AttributeError:
        rating =''
        count = ''
    
    all_record = (name , price , rating , count , url)
    return all_record


# MAIN

url = get_url(search_item)
for page in range(1 , 21):

	webpage = requests.get(get_url(search_item))
	soup = BeautifulSoup(webpage.content , 'html.parser')
	results = soup.find_all('div', {'data-component-type':'s-search-result'})

	for item in results:
		item_data = extract_record(item)
		if item_data:
			records.append(item_data)


with open('results.csv','w', newline='' , encoding='utf-8') as f:
	writer = csv.writer(f)
	writer.writerow(['Name','Price','Rating','Count','URL'])
	writer.writerows(records)

print('DONE')



