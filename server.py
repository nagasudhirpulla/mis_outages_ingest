'''
This is the web server that acts as a service that creates outages raw data
'''
import datetime as dt
from src.appConfig import getConfig
from src.rawDataCreators.outagesRawDataCreator import createOutageEventsRawData
from flask import Flask, request, jsonify
from template import fetchGenUnitOutages
from template import fetchTransElOutages
from template import fetchlongTimeUnrevivedForcedOutages
import cx_Oracle

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

@app.route('/')
def hello():
    return "This is the web server that acts as a service that creates outages raw data"


@app.route('/raw_outages', methods=['POST','GET'])
def create_raw_outages():
    # get start and end dates from post request body
    if request.method=='POST':
        reqData = request.get_json()
        try:
            startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
            endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
        except Exception as ex:
            return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400
        # create outages raw data between start and end dates
        isRawDataCreationSuccess = createOutageEventsRawData(appConfig, startDate, endDate)
        if isRawDataCreationSuccess:
            return jsonify({'message': 'raw data creation successful!!!', 'startDate': startDate, 'endDate': endDate})
        else:
            return jsonify({'message': 'raw data creation was not success'}), 500
    else:
        reqData = request.get_json()
        try:
            startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
            endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
            outageType=reqData['outageType']
            print(startDate,endDate,outageType)
        except Exception as ex:
            return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400
        try:
            if outageType == 'Gen': 
                listOfDict=fetchGenUnitOutages(cx_Oracle.connect(appConfig['appDbConStr']),startDate,endDate)
                # print(listOfDict)
                return jsonify({'message':listOfDict  , 'startDate': startDate, 'endDate': endDate})
            elif outageType == 'Trans':
                listOfDict=fetchTransElOutages(cx_Oracle.connect(appConfig['appDbConStr']),startDate,endDate)
                # print(listOfDict)
                return jsonify({'message':listOfDict  , 'startDate': startDate, 'endDate': endDate})
            else:
                listOfDict=fetchlongTimeUnrevivedForcedOutages(cx_Oracle.connect(appConfig['appDbConStr']),startDate,endDate)
                # print(listOfDict)
                return jsonify({'message':listOfDict  , 'startDate': startDate, 'endDate': endDate})
        except Exception as e:
            return jsonify({'message':'Error occured while fetching data'}),500
        

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
