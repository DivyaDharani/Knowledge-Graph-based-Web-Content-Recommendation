import flask
from flask import jsonify, request
from mining import get_keyword
from main import get_recommendations

from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
CORS(app, support_credentials=True)


# app.config["DEBUG"] = True
@app.route('/', methods=['GET'])
@cross_origin()
def home():
    message = """
    <h1>Data mining API </h1>
    <p>Go to /url and replace <strong>url</strong> in u=<strong>url</strong> with url to get keyword</p>
    """
    return message
@app.route('/url', methods=['GET'])
@cross_origin()
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
@cross_origin()
def get_recommendation():
    request_data = request.get_json()
    recommendations = {}
    print(request_data)
    if request_data and 'value' in request_data and 'request_links' in request_data['value']:
        if (type(request_data['value']['request_links']) == list) and (len(request_data['value']['request_links']) > 0):
            links = request_data['value']['request_links']
            recommendations = get_recommendations(links)
            print(recommendations)

    return jsonify(recommendations)


app.run()
