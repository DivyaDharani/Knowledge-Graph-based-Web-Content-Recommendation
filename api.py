import flask
from flask import jsonify, request
from mining import get_keyword
from main import get_recommendations
app = flask.Flask(__name__)
# app.config["DEBUG"] = True
@app.route('/', methods=['GET'])
def home():
    message = """
    <h1>Data mining API </h1>
    <p>Go to /url and replace <strong>url</strong> in u=<strong>url</strong> with url to get keyword</p>
    """
    return message
@app.route('/url', methods=['GET'])
def url():
    """
    Input data: url
    Return data:
    {
        "description": "A cryptocurrency is a digital or virtual currency that uses cryptography and is difficult to counterfeit.",
        "h1_tag": null,
        "title": "What Is Cryptocurrency?",
        "url": "https://www.investopedia.com/terms/c/cryptocurrency.asp"
    }
    """
    args = request.args
    url = args.get('url')
    if 'url' not in args:
        return "Error: no url. Please input url"
    else:
        keyword = get_keyword(url)
        return jsonify(keyword)


"""
{
    "request_links" : ["link1", "link2", "link3"]
}
"""
@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    request_data = request.get_json()
    recommendation_dict ={}
    print(request_data)
    if request_data and 'request_links' in request_data:
        if (type(request_data['request_links']) == list) and (len(request_data['request_links']) > 0):
            links = request_data['request_links']
            recommended_links = get_recommendations(links)
            print(recommended_links)
            recommendation_dict = {"recommended_links": recommended_links}

    return jsonify(recommendation_dict)

app.run()