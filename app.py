#!/usr/bin/env python
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import pandas as pd

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)


    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

     
    #if req.get("result").get("action") != "facultyAMC":
     #   return {}
    parameters = req.get("result").get("action") 

    if parameters[:7]=='faculty':
       zone =  findFacultyInfo(req,parameters)
    else:
        zone=''
   



    speech=zone

    return {
        "speech": speech,
        "displayText": speech,
 #       "data": {"facebook": facebook_message},
        "source": parameters
    }

def findFacultyInfo(req , faculty):
    data = pd.read_csv('all_faculty2.csv')

    data.set_index("initial", inplace=True) 

    #print faculty
    result = req.get("result")

    query = result.get("resolvedQuery")
    if 'email' in query.lower():
        res = data.loc[[faculty[7:]],'email']
        zone = res[0]

    elif 'office' in query.lower():
        res = data.loc[[faculty[7:]],'office']
        zone = res[0]

    elif 'phone' in query.lower():
        res = data.loc[[faculty[7:]],'phone']
        zone = res[0]

    else:
        res = data.loc[[faculty[7:]],'details']
        zone = res[0] 
    
    return zone


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

   # print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
