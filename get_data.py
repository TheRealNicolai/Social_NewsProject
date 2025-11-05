import time
import tqdm
import json

william, bella, nicolai = 'pub_d9de26b5f5c540558489f00542c6366d', ' ', 'pub_2ffc1a6468d240ee80c80400eeea1c23'

from newsdataapi import NewsDataApiClient
api = NewsDataApiClient(apikey=william)

# pub_d9de26b5f5c540558489f00542c6366d - Williams API
# pub_2ffc1a6468d240ee80c80400eeea1c23 - Nicolai API

all_articles = {}
next_page = None

current_data_file = 'newsdata_p1.json' # None if you don't want to load a current file
new_file_name = 'newsdata_p2.json' # So you don't acidentally overwrite everything

if current_data_file:
    with open(current_data_file, "r", encoding="utf-8") as f:
        all_articles = json.load(f)
        next_page = all_articles['nextPage']

for i in tqdm.tqdm(range(30)):
    time.sleep(3)
    response = api.news_api(language='en', max_result=1000, page=next_page)
    print(response['status'])
    print(response['totalResults'])
    print(response['nextPage'])
    next_page = response['nextPage']
    all_articles['nextPage'] = next_page

    for article in response['results']:
        id = article['article_id']
        if id not in all_articles:
            all_articles[id] = article
        else:
            print(f'id: {id} already processed.')
            
    print(len(all_articles))
    
    with open(new_file_name, 'w') as f:
        json.dump(all_articles, f)