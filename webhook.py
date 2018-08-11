import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response
from datetime import datetime

app = Flask(__name__)


@app.route('/webhook', methods =['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = makeresponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeresponse(req):
    result = req.get('queryResult')
    param = result.get('parameters')
    dateperiod = param.get('date-period')
    date = param.get('date')
    date = date[0:19]
    f = "%Y-%m-%dT%H:%M:%S"
    datetime = datetime.strptime(date, f)
    date = str(datetime)

    city = param.get('geo-city')
    if city is None:
        return None
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=988f06f4fdfda98d437198145dbfe7b5')
    json_object = r.json()
    weather = json_object['list']
    condition =''
    for i in range(0, len(weather)):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break

    speech = "The forecast for "+city+" for date "+date+" is "+condition
    return {
        "fulfillmentText": speech
        #,
#        "displayText": speech,
#        "source": "apiai-weather-webhook"
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('starting app om port ', port)
    app.run(debug=True, port=port, host='0.0.0.0')
