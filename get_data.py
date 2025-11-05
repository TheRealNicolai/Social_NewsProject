import time
import tqdm
import json

from newsdataapi import NewsDataApiClient

def get_new_articles(api_key, current_data_file = None, output_data_file = None):
    api = NewsDataApiClient(apikey=api_key)

    all_articles = {}
    next_page = None

    if current_data_file:
        with open(current_data_file, "r", encoding="utf-8") as f:
            all_articles = json.load(f)
            next_page = all_articles['nextPage']

    for i in tqdm.tqdm(range(30)):
        time.sleep(3)
        response = api.news_api(language='en', max_result=1000, page=next_page)
        print()
        print(f'Status: {response['status']}')
        print(f'total results: {response['totalResults']}')
        print(f'next page: {response['nextPage']}')
        next_page = response['nextPage']
        all_articles['nextPage'] = next_page

        for article in response['results']:
            id = article['article_id']
            has_metadata = True
            metadata_list = ['link', 'title', 'description', 'country', 'category', 'pubDate', 'source_id', 'source_name']
            for metadata in metadata_list:
                if not article[metadata]:
                    has_metadata = False
                    break
            if has_metadata and id not in all_articles and not article['duplicate'] and article['language'] == 'english':
                article_relevant = {metadata : article[metadata] for metadata in metadata_list}
                all_articles[id] = article_relevant
            else:
                print(f'id: {id} not valid.')
                
        print(f'Total articles so far: {len(all_articles)-1}')
        
        if output_data_file:
            with open(output_data_file, 'w') as f:
                json.dump(all_articles, f)
            
if __name__ == '__main__':
    william, bella, nicolai = 'pub_d9de26b5f5c540558489f00542c6366d', ' ', 'pub_2ffc1a6468d240ee80c80400eeea1c23'
    
    get_new_articles(william, current_data_file='newsdata_p1.json', output_data_file='newsdata_p2.json')