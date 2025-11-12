import json
import pickle
from tqdm import tqdm

from sentence_transformers import SentenceTransformer

def embed_articles(input_filename = 'newsdata.json', embedding_variables = ['description', 'title']):

    model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, good balance. 'multi-qa-MiniLM-L6-cos-v1' is another good option tuned for semantic search.

    with open(input_filename, "r", encoding="utf-8") as f:
        all_articles = json.load(f)
        
    embedded_articles = {}
    num_not_valid = 0
    for id, article in tqdm(all_articles.items()):
        if id == 'nextPage':
            continue
        valid_article = True
        for embedding_variable in embedding_variables:
            if not article[embedding_variable]:
                valid_article = False
                num_not_valid += 1
                break
        if valid_article:
            embedded_articles[id] = article
            for embedding_variable in embedding_variables:
                embedding = model.encode(article[embedding_variable], normalize_embeddings=True)
                embedded_articles[id][f'embedded_{embedding_variable}'] = embedding
    print(f'Number of articles not valid for embedding: {num_not_valid}')
    return embedded_articles, len(embedding), (len(all_articles)-1)
    
if __name__ == '__main__':
    embedding_variables = ['description', 'title']
    input_filename = 'newsdata.json'
    output_filename = 'embedded_articles.pkl'
    embedded_articles, embedding_length, all_articles_length = embed_articles()

    with open(output_filename, 'wb') as f:
        pickle.dump(embedded_articles, f)

    print(f'Embedding size: {embedding_length}')
    print(f'Length of all_articles (minus nextPage): {all_articles_length}')
    print(f'Length of embedded_articles: {len(embedded_articles)}')