import wikipediaapi
def search_wiki(url):
    paragraph_length = 250
    keyword = url.split("/")
    keyword = keyword[-1]
    # print(keyword)
    wiki_wiki = wikipediaapi.Wikipedia('en')

    page_py = wiki_wiki.page(keyword)
    result = page_py.summary[0:paragraph_length]
    return result
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Lionel_Messi"
    search_wiki(url)
