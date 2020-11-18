try:
    import urllib
    import json
    import os
    import csv
    import pandas as pd
    from flask import (Flask,request,jsonify, make_response, render_template)
    from flask_mail import Mail,Message

except Exception as e:

    print("Some modules are missing {}".format(e))

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "<your_gmail.com>"
app.config['MAIL_PASSWORD'] = "<password>"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=['GET'])
def ping():
    return ("hello world")


@app.route('/webhook', methods=['POST','GET'])
def webhook():

    #if request.method == "POST":
    req = request.get_json(silent=True, force=True)    # build a request object
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



def processRequest(req):

    # Get all the Query Parameter
    query_response = req["queryResult"]
    # print(query_response)
    text = query_response.get('queryText', None)
    parameters = query_response.get('parameters', None)   #fetch parameters from json

    res = ""

    if req['queryResult']["intent"]["displayName"] == "Default Welcome Intent":
        res = get_welcome_response(req)

    if req['queryResult']["intent"]["displayName"] == "service.types":
        res = get_service_type_response(req, parameters)


    if req['queryResult']["intent"]["displayName"] == "others":
        send_message(parameters)
        return 'res'



def get_welcome_response(req):


    print(req['queryResult']['fulfillmentText'])
    speech = "Welcome to test app."

    return {
        "fulfillmentText": speech,
    }

def get_service_type_response(req, parameters):
    from pprint import pprint
    pprint(parameters)

    speech = " Webhook Response! "

    return {
        "fulfillmentText": speech,
    }


def send_message(parameters):
    if request.method == "POST":
         #"{queryRsult:{}}" {queryREsult:{}}

        email=parameters['email']

        print(email,"successful")

        subject = "<Message>"
        msg = "This is test case please ignore it <Paste the html template here>"

        message = Message(subject,sender="<your_gmail.com>",recipients=[email])

        message.body = msg

        mail.send(message)

    return jsonify({'Status':'OK'})



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='localhost')

