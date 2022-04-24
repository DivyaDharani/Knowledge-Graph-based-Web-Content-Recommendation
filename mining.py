import requests
from bs4 import BeautifulSoup

def get_keyword(url):
    # Check the schema
    if "https://" not in url and "http://" not in url:
        url = "https://" + url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = {"url":"", "title":"", "description":"", "h1_tag":""}
    # Get the meta data
    title = soup.find("meta", property="og:title")
    url = soup.find("meta", property="og:url")
    description = soup.find("meta", property="og:description")
    title = title["content"] if title else "No meta title given"
    url = url["content"] if url else "No meta url given"
    description = description["content"] if description else "No meta url given"
    # Get the p tag
    h1_tag = soup.find("h1")
    h1_tag = h1_tag.text
    # Construct result
    result["url"] = url
    result["title"] = title
    if not description:
        result["h1_tag"] = h1_tag
        result["description"] = None
        return result
    result["h1_tag"] = None
    result["description"] = description
    return result


def extract_text(links):
    sentence_list = []
    for link in links:
        result = get_keyword(link)
        if result["description"] is not None:
            sentence_list.append(result["description"])
        elif result["h1_tag"] is not None:
            sentence_list.append(result["h1_tag"])
    return sentence_list

