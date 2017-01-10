#newapp1.py

from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json

app= Flask(__name__)

app.config['MONGO_DBNAME']= 'coordinates'
app.config['MONGO_URL']= 'mongodb://localhost:27017/coordinates'
#url= 'http://ec2-35-162-91-20.us-west-2.compute.amazonaws.com:1100/post/1/1/1'
mongo= PyMongo(app)
#_,identifier,xcoordinate,ycoordinate,zcoordinate= url.split('/',4)
@app.route('/post', methods=['POST'])
def add_coordinate():
           #return "Hello world"
           xcoordinate=0
           ycoordinate=0
           zcoordinate=0
           coordinate= mongo.db.coordinates
           #retur
           #return request.json
           #data= request.get_json()
           #xcoordinate= request.args.get('xcoordinate',1,type=int)
           xcoordinate= request.json["xcoordinate"]
           ycoordinate= request.json["ycoordinate"]
           zcoordinate= request.json["zcoordinate"]
           #return xcoordinate
          # print xcoordinate
           #ycoordinate= request.args.get('ycoordinate',1,type=int)
           #zcoordinate= request.args.get('zcoordinate',1,type=int)
           coordinate.insert({'xcoordinate': xcoordinate, 'ycoordinate': ycoordinate, 'zcoordinate': zcoordinate})
           new_coordinate=coordinate.find_one({'xcoordinate': xcoordinate} and {'ycoordinate':ycoordinate} and {'zcoordinate':zcoordinate})
           output = {'xcoordinate': new_coordinate['xcoordinate'],'ycoordinate':new_coordinate['ycoordinate'], 'zcoordinate':new_coordinate['zcoordinate']}

           return jsonify({'result':output})

@app.route('/get', methods=['GET'])
def get_coordinate():
           coordinate= mongo.db.coordinates
           output= []
           for c in coordinate.find():
                      output.append({'xcoordinate': c['xcoordinate'], 'ycoordinate': c['ycoordinate'], 'zcoordinate': c['zcoordinate']})
@app.route('/get', methods=['GET'])
def get_coordinate():
           coordinate= mongo.db.coordinates
           output= []
           for c in coordinate.find():
                      output.append({'xcoordinate': c['xcoordinate'], 'ycoordinate': c['ycoordinate'], 'zcoordinate': c['zcoordinate']})
           return jsonify({'result' : output})

#@app.route('/graph1')
#def graph1(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
#           chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
#           coordinate= mongo.db.coordinates
#           L =list()
#
#           for c in coordinate.find():
#                       output.append({'xcoordinate':c['xcoordinate'], 'ycoordinate': c['ycoordinate'], 'zcoordinate': c['zcoordinate']})
#          i=0
#          for i<100:
#                       series = [{"name": 'Label1', "data": c['xcoordinate']}, {"name": 'Label2', "data":  c['ycoordinate']}, {"name": 'Label3', "data": c['zcoordinate']}]
#          title = {"text": 'My Title'}
#           xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
#           yAxis = {"title": {"text": 'yAxis Label'}}
#           return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/graph')
def graph(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
           chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
           coordinate = mongo.db.coordinates
           for c in coordinate.find():
 L = list()
                      series =  [{"name": 'Label1', "data":c ['xcoordinate']}, {"name": 'Label2', "data": ['ycoordinate']}, {"name": 'Label3', "data": c['zcoordinate']}]
                      title = {"text": 'my Title'}
                      xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
                      yAxis = {"title": {"text": 'yAxis Label'}}
                      return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

if __name__== '__main__':
           app.run(debug=True, host="0.0.0.0", port= 80)



