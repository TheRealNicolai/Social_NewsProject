import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import nltk
from statistics import mean, median, variance, quantiles
import re


def calculate_sentiment_score(article_string: str, happiness_ranks):
    # Tokenize page
    remove_punc = re.sub(r'[^\w\s]', ' ', article_string)
    clean_text = re.sub(r'\s+', ' ', remove_punc).strip()
    text_lower = clean_text.lower()
    content = [w for w in text_lower.split() if w.isalpha()] #extract words from string

    # Calculate frequency of words
    fdist = nltk.FreqDist(content)

    # Calculate sentiment
    weighted_sentiment_score = 0
    count = 0
    for w, f in fdist.items():
        try:
            idx = np.where(happiness_ranks.word == w.lower())
            idx = idx[0][0]
            weighted_sentiment_score += happiness_ranks['happiness_average'].iloc[idx]*f
            count += f
        except:
            continue
    
    if weighted_sentiment_score > 0:
        return weighted_sentiment_score/count, content
    else:
        return None, content


def save_sentiment_scores(all_articles: dict):

    # Load labMT
    happiness_ranks = pd.read_csv("labMT.txt", sep='\t', skiprows = lambda x: x in [0,1,2], index_col = False)

    sentiments_title = {}
    sentiments_description = {}
    wl_title = {}
    wl_description = {}

    count_no_title = 0
    count_no_description = 0

    for key, article in all_articles.items():
        try:
            title = article['title']
            # List of words of each article title is saved in wl_titles
            sentiment, wl_title[key] = calculate_sentiment_score(title, happiness_ranks)
            if sentiment is None:
                count_no_title +=1
            else:
                sentiments_title[key] = sentiment
        except:
            print(f"Could not calculate sentiment for title of {key}")

        try:
            description = article['description']
            # List of words of each article description is saved in wl_description
            sentiment, wl_description[key] = calculate_sentiment_score(description, happiness_ranks)
            if sentiment is None:
                count_no_description +=1
            else:
                sentiments_description[key] = sentiment
        except:
            print(f"Could not calculate sentiment for title of {key}")

    return sentiments_title, sentiments_description, wl_title, wl_description

def count_emotional_words(all_articles: dict, wl: dict, title = True):

    # https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm
    path_emotions = "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
    emotion_scores = pd.read_csv(path_emotions, sep='\t', index_col = False, header= None, names = ['word', 'emotion', 'associated'])

    if title:
        articles_title_emotions = {}
        articles_title_no_emotions = 0
    
    else:
        articles_description_emotions = {}
        articles_description_no_emotions = 0

    for article_id in all_articles.keys():
        content = wl[article_id]
        article_emotions = {}
        for word in content:
            if word in emotion_scores.word.values:
                try:
                    subset = emotion_scores[(emotion_scores.word == word) & (emotion_scores.associated == 1) ]['emotion']
                    for e in subset:
                        if e not in article_emotions:
                            article_emotions[e] = 1
                        else:
                            article_emotions[e] += 1
                except:
                    continue

        if title:
            if len(article_emotions)>0:
                articles_title_emotions[article_id] = article_emotions
            else:
                articles_title_no_emotions += 1
        else:
            if len(article_emotions)>0:
                articles_description_emotions[article_id] = article_emotions
            else:
                articles_description_no_emotions += 1
    
    if title:
        return articles_title_emotions, articles_title_no_emotions
    else:
        return articles_description_emotions, articles_description_no_emotions

def sentiment_scores():
    # Load articles and 
    with open("newsdata.json", "r", encoding="utf-8") as f:
        all_articles = json.load(f)
    all_articles.pop('nextPage')

    sentiments_title, sentiments_description, wl_title, wl_description = save_sentiment_scores(all_articles)

    print('calculated sentiment score')

    articles_title_emotions, articles_title_no_emotions = count_emotional_words(all_articles, wl_title, title=True)
    articles_description_emotions, articles_description_no_emotions = count_emotional_words(all_articles, wl_description, title=False)

    print('counted emotional words')
    
    print(f"{articles_title_no_emotions} article titles have no emotional words")
    print(f"{articles_description_no_emotions} article descriptions have no emotional words")

    #Save data
    with open("sentiments_title.json", "w") as f:
        json.dump(sentiments_title, f)

    with open("sentiments_description.json", "w") as f:
        json.dump(sentiments_description, f)

    with open("wl_title.json", "w") as f:
        json.dump(wl_title, f)

    with open("wl_description.json", "w") as f:
        json.dump(wl_description, f)

    with open("articles_title_emotions.json", "w") as f:
        json.dump(articles_title_emotions, f)

    with open("articles_description_emotions.json", "w") as f:
        json.dump(articles_description_emotions, f)
    
    print('Saved data as json')

if __name__=="__main__":
    sentiment_scores()
