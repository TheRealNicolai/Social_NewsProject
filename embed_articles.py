import json
import pickle
import tqdm

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, good balance

embedding_variables = ['description', 'title']

input_filename = 'newsdata_p1.json'
output_filename = 'embedded_articles.pkl'

with open(input_filename, "r", encoding="utf-8") as f:
    all_articles = json.load(f)
    
    
embedded_articles = {}
for id, article in tqdm.tqdm(all_articles.items()):
    if id == 'nextPage':
        continue
    valid_article = True
    for embedding_variable in embedding_variables:
        if not article[embedding_variable]:
            valid_article = False
            break
    if valid_article:
        embedded_articles[id] = article
        for embedding_variable in embedding_variables:
            embedding = model.encode(article[embedding_variable], normalize_embeddings=True)
            embedded_articles[id][f'embedded_{embedding_variable}'] = embedding
            

with open(output_filename, 'wb') as f:
    pickle.dump(embedded_articles, f)
    
if __name__ == '__main__':
    print(f'Embedding size: {len(embedding)}')
    print(f'Length of all_articles (minus nextPage): {len(all_articles)-1}')
    print(f'Length of embedded_articles: {len(embedded_articles)}')