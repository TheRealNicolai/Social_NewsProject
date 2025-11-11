import numpy as np
from numpy.linalg import norm
import pickle
from tqdm import tqdm

def cosine_sim(input_data, epsilon=1e-10):
    # Checking if numpy array
    if not isinstance(input_data, np.ndarray):
        input_data = np.array(input_data)
    # Calculating cosine similarities for all rows with one another.
    cos_sim = np.zeros((input_data.shape[0], input_data.shape[0]))
    for i, row in tqdm(enumerate(input_data), total=len(input_data)):
        for j, row2 in enumerate(input_data):
            cos_data = np.dot(row, row2) / (norm(row) * norm(row2) + epsilon)
            cos_sim[i][j] = cos_data
    return cos_sim

if __name__ == '__main__':
    with open('embedded_articles.pkl', 'rb') as f:
        embedded_articles = pickle.load(f)
    
    emb_titles = []
    emb_desc = []
    for key in embedded_articles.keys():
        emb_titles.append(embedded_articles[key]['embedded_title'])
        emb_desc.append(embedded_articles[key]['embedded_description'])
    
    cossim_title = cosine_sim(emb_titles)
    cossim_desc = cosine_sim(emb_desc)

    with open('cosine_similarities_titles.pkl', 'wb') as f:
        pickle.dump(cossim_title, f)

    with open('cosine_similarities_descriptions.pkl', 'wb') as f:
        pickle.dump(cossim_desc, f)