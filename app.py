from flask import Flask,request, jsonify, json, abort
from flask_cors import CORS, cross_origin
import time,pymongo
from mongodb import MongodbOperator
import datetime ,operator

mongodb_addr = '139.219.64.238'
mongodb_port = 27017
mongodb_username = 'c004517c-2d95-498c-a5c7-900f22620314'
mongodb_passwd = 'EvoPzLheHf10iudSDag83WbSi'
mongodb_Database = '1cdc85b4-8fda-4361-be1c-9ccb588ddd5e'
mongodb_collection = 'common_Modbus_Handler'

PatacMongodb = MongodbOperator(mongodb_addr, mongodb_port, mongodb_username, mongodb_passwd, mongodb_Database,
                       mongodb_collection)
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
methods = ('GET', 'POST')

metric_readers = {}
annotation_readers = {}
panel_readers = {}

def dget(dictionary, cmd, default=None):
    cmd_list = cmd.split('.')
    tmp = dict(dictionary)
    for c in cmd_list:
        try:
            val = tmp.get(c, None)
        except AttributeError:
            return default
        if val!= None:
            tmp = val
        else:
            return default
    return tmp

def datetime_timestamp(dt):
    time.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ')
    s = time.mktime(time.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ'))
    return int(s)



@app.route('/', methods=methods)
@cross_origin()
def index():
    print("++++++++++++++++++++++++++++++++")
    print(request.headers, request.get_json())
    print("++++++++++++++++++++++++++++++++")
    return 'ok'

@app.route('/search',methods=methods)
@cross_origin()
def grafana_search():
    print("++++++++++++++++++++++++++++++++")
    print("headers:", request.headers, request.get_json())
    print("++++++++++++++++++++++++++++++++")
    req = request.get_json()
    target = req.get('target', '*')
    metric = ['Temperature', 'Humidity']
    return jsonify(metric)

@app.route('/query',methods=methods)
@cross_origin()
def grafana_query():
    print("++++++++++++++++++++++++++++++++")
    print("headers:", request.headers, request.get_json())
    print("++++++++++++++++++++++++++++++++")
    query_data = {}
    datapoint = []
    req = request.get_json()
    from_time = datetime_timestamp(dget(req, 'range.from'))
    to_time = datetime_timestamp(dget(req, 'range.to'))
    print('from_time', from_time)
    print("to_time=", to_time)
    targets = req.get('targets')
    target = targets[0].get('target')

    if operator.eq(target,'Temperature'):
        for record in PatacMongodb.find_db({'agentId': '00000001-0000-0000-0000-C400AD036584',
                                "sensorId": "/Holding Registers/eTempSample",
                                "ts": {"$gte": datetime.datetime.fromtimestamp(from_time),
                                       "$lte":datetime.datetime.fromtimestamp(to_time)}}):
            Temp_Value=record.get('v')
            ts = ((record.get('ts').timestamp()+28800)*1000)
            temp = [Temp_Value,ts]
            datapoint.append(temp)

    if operator.eq(target,'Humidity') :
        for record in PatacMongodb.find_db({'agentId': '00000001-0000-0000-0000-C400AD036584',
                                "sensorId": "/Holding Registers/eHumiditySample",
                                "ts": {"$gte": datetime.datetime.fromtimestamp(from_time),
                                       "$lte":datetime.datetime.fromtimestamp(to_time)}}):
            Humi_Value=record.get('v')
            ts = ((record.get('ts').timestamp()+28800) * 1000)
            temp =[Humi_Value,ts]
            datapoint.append(temp)


    query_data=[{"target":target,"datapoints":datapoint}]
    return jsonify(query_data)

if __name__ == '__main__':
    app.run()
