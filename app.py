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

    #print parameters

    if parameters[:7]=='faculty':
       zone =  findFacultyInfo(req,parameters)
    elif parameters == 'coursePre':
        zone = findCourseInfo(req,parameters)
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

    param = result.get("parameters")
    p = param.get("faculty")

    #print p
    if 'email' in query.lower():
        res = data.loc[[p],'email']
        zone = res[0]

    elif 'office' in query.lower():
        res = data.loc[[p],'office']
        zone = res[0]

    elif 'contact' in query.lower():
        res = data.loc[[p],'office']
        zone = res[0]

    elif 'room' in query.lower():
        res = data.loc[[p],'office']
        zone = res[0]
        
    elif 'mobile' in query.lower():
        res = data.loc[[p],'phone']
        zone = res[0]

    elif 'phone' in query.lower():
        res = data.loc[[p],'phone']
        zone = res[0]

    else:
        res = data.loc[[p],'details']
        zone = res[0] 
    
    return zone

def findCourseInfo(req , faculty):
    data = pd.read_csv('allCourse.csv')

    data.set_index("code", inplace=True) 

    #print faculty
    result = req.get("result")


    param = result.get("parameters")
    p = param.get("Course")

    courseCode=p
    res2=courseCode+" : "
    res3 = data.loc[[courseCode],'name']
    res4=  data.loc[[courseCode],'credit']
    res5 = data.loc[[courseCode],'pre'] 

    result = str(res2) + str(res3[0]) + "\nCredit Hours : " + str(res4[0]) +" \nPre-requisites : " + str(res5[0])

    labCourse = " 115 215 225 231 311 331 141 111 211 241 312 321 342 362 363 321 331 424 426 471 "
    #print courseCode[4:]

    if courseCode[3:] in labCourse:
        courseCode = courseCode+"L"
        res2=courseCode+" : "
        res3 = data.loc[[courseCode],'name']
        res4=  data.loc[[courseCode],'credit']
        res5 = data.loc[[courseCode],'pre']
        print (res2)
        print (res3)
        print (res4)
        result= result+"\nLab Course for this course:\n"+ str(res2) + str(res3[0]) + "\nCredit Hours : " + str(res4[0]) +" \nPre-requisites : " + str(res5[0])


    finalResult= result + "\nNote : No courses can take without prerequisite .\nFor details see this link http://ece.northsouth.edu/undergraduate/academics/programs/"
    
    #print finalResult

    return finalResult


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

   # print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
