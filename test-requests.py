import requests

"""
request_links = ["link1", "link2", "link3"]

returned result
recommendation_dict = {'links': ['link1', 'link2', 'link3']}
links_recommended = ['link1', 'link2', 'link3']
"""

def request_recommendation(links):
    request_json = {"request_links": links}
    response = requests.post('http://127.0.0.1:5000/recommendation', json=request_json)
    links_recommended = []
    print(response)
    #print(response.json())
    if response.status_code == 200:
        recommendation_dict = response.json()

        if recommendation_dict is not None and "recommended_links" in recommendation_dict:
            links_recommended = recommendation_dict["recommended_links"]

    return links_recommended


request_links = ['https://www.investopedia.com/terms/c/cryptocurrency.asp', 'https://en.wikipedia.org/wiki/Lionel_Messi', 'https://en.wikipedia.org/wiki/Elon_Musk', 'https://en.wikipedia.org/wiki/Barack_Obama', 'https://en.wikipedia.org/wiki/Ukraine', 'https://en.wikipedia.org/wiki/Pacific_Ocean']

print(request_recommendation(request_links))