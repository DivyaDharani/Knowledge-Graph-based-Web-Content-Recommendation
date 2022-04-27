import requests

"""
request_links = ["link1", "link2", "link3"]

returned result
{'Anime': [['Lupin III Part III', 'Hyōga Senshi Gaislugger', 'Phanton Thief Reinya']], 'City': [['Ar Rutba', 'Port Loko', 'Port Mathurin']]}

"""

def request_recommendation(links):
    request_json = {"request_links": links}
    response = requests.post('http://127.0.0.1:5000/recommendation', json=request_json)
    recommendation_dict = {}
    print(response)
    if response.status_code == 200:
        recommendation_dict = response.json()

    return recommendation_dict


request_links = ['https://www.investopedia.com/terms/c/cryptocurrency.asp',
                 'https://en.wikipedia.org/wiki/Lionel_Messi',
                 'https://en.wikipedia.org/wiki/Elon_Musk',
                 'https://en.wikipedia.org/wiki/Barack_Obama',
                 'https://en.wikipedia.org/wiki/Ukraine',
                 'https://en.wikipedia.org/wiki/Pacific_Ocean']

request_links2 = ['https://en.wikipedia.org/wiki/Tesla,_Inc.',
                  'https://en.wikipedia.org/wiki/Croissant',
                  'https://en.wikipedia.org/wiki/Republican',
                  'https://en.wikipedia.org/wiki/Elon_Musk',
                  'https://en.wikipedia.org/wiki/Eiffel_Tower',
                  'https://en.wikipedia.org/wiki/Christmas']

request_links3 = ['https://towardsdatascience.com/knowledge-data-science-with-semantics-technologies-ff54e4fe306c',
                  'https://medium.com/starts-with-a-bang/the-simplest-explanation-of-global-warming-ever-2b365aff0c2f',
                  'https://medium.com/starts-with-a-bang/tagged/black-holes',
                  'https://www.investopedia.com/terms/c/cryptocurrency.asp',
                  'https://towardsdatascience.com/tagged/python']

print(request_recommendation(request_links2))