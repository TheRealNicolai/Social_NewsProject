import time
import json
from tqdm import tqdm

from newsdataapi import NewsDataApiClient, newsdataapi_exception

def get_new_articles(api_key, data_filename = None, verbose=False):
    api = NewsDataApiClient(apikey=api_key)

    all_articles = {}
    next_page = None

    if data_filename:
        with open(data_filename, "r", encoding="utf-8") as f:
            all_articles = json.load(f)
            next_page = all_articles['nextPage']
    
    start_n_articles = len(all_articles)

    for i in tqdm(range(30)):
        time.sleep(3)
        try:
            response = api.news_api(language='en', max_result=1000, page=next_page)
        except newsdataapi_exception.NewsdataException:
            response = api.news_api(language='en', max_result=1000, page=None)
            if verbose:
                print('\nGetting page from new day.')
        if verbose:
            print()
            print(f'Status: {response["status"]}')
        next_page = response['nextPage']
        all_articles['nextPage'] = next_page

        for article in response['results']:
            id = article['article_id']
            missing_metadata = False
            metadata_list = ['link', 'title', 'description', 'country', 'category', 'pubDate', 'source_id', 'source_name']
            for metadata in metadata_list:
                if not article[metadata]:
                    if not missing_metadata:
                        missing_metadata = [metadata]
                    else:
                        missing_metadata.append(metadata)
            already_processed = False
            if not missing_metadata and id in all_articles:
                already_processed = True
            duplicate_article = False
            if not missing_metadata and not already_processed and article['duplicate']:
                duplicate_article = True
            english = True
            if not missing_metadata and not already_processed and not duplicate_article and article['language'] != 'english':
                english = False
            multiple_countries = False
            if not missing_metadata and not already_processed and not duplicate_article and english and len(article['country']) != 1:
                multiple_countries = True
            country_is_world = False
            if not missing_metadata and not already_processed and not duplicate_article and english and not multiple_countries and article['country'][0] == 'world':
                country_is_world = True
            if not missing_metadata and not already_processed and not duplicate_article and english and not multiple_countries and not country_is_world:
                article_relevant = {metadata : article[metadata] for metadata in metadata_list}
                all_articles[id] = article_relevant
            elif verbose:
                error_string = ""
                if missing_metadata:
                    error_string = f"missing metadata {missing_metadata}"
                elif already_processed:
                    error_string = "the article id already being processed"
                elif duplicate_article:
                    error_string = "the article being a duplicate"
                elif not english:
                    error_string = "the article not being in english"
                elif multiple_countries:
                    error_string = "the article belonging to multiple countries"
                elif country_is_world:
                    error_string = "the country being 'world'"
                print(f'id: {id} not valid due to {error_string}.')
                
        if verbose:
            print(f'Total results: {response["totalResults"]}')
            print(f'Next page: {response["nextPage"]}')
            print(f'Total articles so far: {len(all_articles)-1}')
        
        if len(all_articles) > start_n_articles:
            with open(data_filename, 'w') as f:
                json.dump(all_articles, f)
                
    added_articles = len(all_articles) - start_n_articles
    print(f'Added {added_articles} articles to dataset')
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f'End time: {formatted_time}')
            
if __name__ == '__main__':
    william, bella, nicolai = 'pub_d9de26b5f5c540558489f00542c6366d', 'pub_b17b6c07e5924b47a7266d5a23f43a33', 'pub_2ffc1a6468d240ee80c80400eeea1c23'
    
    get_new_articles(william, data_filename='newsdata.json', verbose=True)