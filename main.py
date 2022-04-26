from mining import extract_text
from web_recommendation import recommend_web_articles

def get_recommendations(links):
    texts = extract_text(links)
    print(texts)
    recommended_links = recommend_web_articles(texts)
    return recommended_links