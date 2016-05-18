import csv
import config
from datetime import datetime, timedelta

#Defines the user class, a user is one potential or complete survey subject
class User:
   def __init__(self):
      self.email = ''
      self.state = 'n'
      self.parentID = ''
      self.childrenID = ['']*len(config.survey1questions)
      self.survey = ''
      self.selectTime = datetime.now() - timedelta(days=100)
      self.sendTime = datetime.now() - timedelta(days = 100)
      self.returnTime = datetime.now() - timedelta(days = 100)

#Open the csv and write to it the current user array
def writecsv(users,filename):
   with open(filename, 'w') as csvfile:
      writer = csv.writer(csvfile, delimiter = ',')
      writer.writerows(users)
#read the csv. The users will be parsed elsewhere
def readcsv(filename):
   file = open(filename, 'r')
   datareader = csv.reader(file,delimiter=',')
   d = []
   for row in datareader:
      d.append(row)
   return d 

#Transfer and array of user objects to a 2d array to be put into
#the csv
def usersToArray(users):
   xran = len(users)
   yran = 7+ len(users[0].childrenID)
   d = [['' for x in range(yran)] for x in range(xran)]
   for i in range (0,xran):
      d[i][0] = users[i].email
      d[i][1] = users[i].state
      d[i][2] = users[i].parentID
      a = 0
      for j in range(3, 3 + len(users[i].childrenID)):
         d[i][j] = users[i].childrenID[j-3]
         a = j + 1
      d[i][a] = users[i].survey
      d[i][a+1] = users[i].selectTime.strftime('%Y-%m-%d %H:%M:%S')
      d[i][a+2] = users[i].sendTime.strftime('%Y-%m-%d %H:%M:%S')
      d[i][a+3] = users[i].returnTime.strftime('%Y-%m-%d %H:%M:%S')
   return d


#Given an array from the csv, initialize an array of user objects
def arrayToUsers(arr):
   xran = len(arr)
   users = []
   for i in range(0,len(arr)):
      user = User()
      user.email = arr[i][0]
      user.state = arr[i][1]
      user.parentID = arr[i][2]
      a = len(user.childrenID) + 3
      for j in range(3,len(user.childrenID)):
         user.childrenID[j-3] = arr[i][j]
      user.survey = arr[i][a]
      user.selectTime = datetime.strptime(arr[i][a+1], '%Y-%m-%d %H:%M:%S')
      user.sendTime = datetime.strptime(arr[i][a+2], '%Y-%m-%d %H:%M:%S')
      user.returnTime = datetime.strptime(arr[i][a+3], '%Y-%m-%d %H:%M:%S')
      users.append(user)
   return users
   
