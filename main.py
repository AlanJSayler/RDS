#Main 'run through' of the program. This is run periodically
#to update the state of the file to match what has happened on 
#Qualtrics, as well as to send out new surveys in accordance
#with how many have expired or been completed

import urllib
import config
import quapi
import parsers
import helpers
import filemanager
import os
from datetime import datetime, timedelta
#load config.
config.init()
curDir = os.path.dirname(__file__)
#read old validation file, exit if it's bad
valPath = os.path.join(curDir, 'validation.txt')
validation = filemanager.readcsv(valPath)
if validation[0][0] != 'GOOD':
   print(validation[0][0])
   print('Something went wrong at ' + str(datetime.now()) + ', stopping')
   exit()

validation[0][0] = 'BAD'
filemanager.writecsv(validation, valPath)

#read old csv to get data.
csvPath = os.path.join(curDir, config.fileName)
arr =  filemanager.readcsv(csvPath)
users = filemanager.arrayToUsers(arr)
precount = 0
#count how many completed surveys there were at the end of the last run
for i in range(0,len(users)):
   if users[i].state == 'c':
      preCount = preCount +1


#query qualtrics for responses
#TODO This part needs to be changed to accomodate more than two surveys
#It's silly to have essentially the same line twice, let's generalize it.
xmlResp1 = quapi.makeRequest(quapi.getLegacyResponseData(
           config.survey1ID, config.survey1Questions))
xmlResp2 = quapi.makeRequest(quapi.getLegacyResponseData(
           config.survey2ID,config.survey2Questions))

#TODO This part needs to be changed to accomodate more than two surveys
#It's silly to have essentially the same line twice, let's generalize it.
arr1 = parsers.parseForEmails(xmlResp1,config.survey1Refs)
arr2 = parsers.parseForEmails(xmlResp2,config.survey2Refs)

#integratge new responses with old data, set repeats and invalids to D, 
#set completed surveys to C, send them thank yous
#TODO Generalize this to more than two surveys
for(d in range(0,2):
   currSurv = arr1
   if(d == 1)
       currSurv = arr2
   for i in range(0,len(currSurv)):
      for j in range(0,len(users)):
         if currSurv[i][0] == users[j].email:
            users[j].state = 'c'
            for k in range(0,len(users[j].childrenID)):
               users[j].childrenID[k] = currSurv[i][k+1]
               if users[j].childrenID[k] == None:
                  users[j].childrenID[k] = ''
               users[j].childrenID[k] = users[j].childrenID[k].replace(' ', '')

#count number of completed surveys in integrated list
postCount = 0
for i in range(len(users)):
   if users[i].state == 'c':
      postCount = postCount + 1

#calculate number of 'credits' or number or maximum possible
#new surveys to be sent this round
credits = (postCount - preCount) * config.creditsForCompletions
#kill all nonvalid surveys
if config.allowOnlySuffixes == 1:
   for i in range(0,len(users)):
      if config.suffix not in users[i].email:
         users[i].state == 'd'
for i in range(0,len(users)):
   invalid =  '~`!#$%^&*()_-+={}[]:>;\',</?*-+'
   for j in users[i].email:
      for k in invalid:
         if j ==k:
            users[i].state = 'd'

#kill expired surveys
for i in range(len(users)):
   if ((users[i].sendTime + config.expiry) < datetime.now() 
      and users[i].state == 's'):
      print('killed expired survey belonging to '+  users[i].email + 'at'
           + users[i].sendTime)
      users[i].state = 'd'
      credits = credits + 1

#add children to the list of users
for i in range(0, len(users)):
   if users[i].state == 'c':
      for j in range(0, len(users[i].childrenID)):
         found = 0
         for k in range(0, len(users)):
            if users[i].childrenID[j] == users[k].email:
               found = 1
         if found == 0:
            if users[i].childrenID[j]:
               new = filemanager.User()
               new.email = users[i].childrenID[j]
               new.email = new.email.replace(' ', '')
               new.parentID = users[i].email
               new.state = 'n'
               users.append(new)


#check for Qs more than 1 day old, send surveys, set state to S
for i in range(0,len(users)):
   if (users[i].state == 'q' 
      and datetime.now() > (users[i].selectTime + config.delay)):
      surv = helpers.chooseSurvey()
      subj = ''
      if users[i].parentID == '' or config.altSubject == 1:
         subj = config.subject
      else:
         subj = config.subject2 + users[i].parentID
      quapi.sendSurveySubjectExpiry(users[i].email, surv,subj) 
      users[i].state = 's'
      users[i].sendTime = datetime.now()   
      users[i].survey = surv
#calculate ave distance of each N to Qs and Ss and Cs
listofListOfParents = [None] *len(users)
dists = [0] * len(users)
for i in range(0,len(users)):
   listofListOfParents[i] = helpers.getParentList(users,i)
for i in range(0,len(users)):  
   if users[i].state == 'n':
      if not users[i].parentID:
         dists[i] = 10000
      else:
          
         for j in range(0,len(users)):
            if (users[j].state == 's'or users[j].state == 'c' 
               or users[j].state == 'q'):
               dists[i] = (dists[i] +  helpers.calcDist(
                          listofListOfParents[i],listofListOfParents[j]))
#Count the total number of eligible surveys for denominator
running = 0
for i in range(0,len(users)):
   if users[i].state == 's' or users[i].state == 'c' or users[i].state == 'q':
      running = running +1
#set Ns to Qs until either credits, or total coupons are exceeded.
credits = 0
while credits > 0 and running < config.total:
   index = dists.index(max(dists))
   if users[index].state == 'n':
      users[index].state = 'q'
      users[index].selectTime = datetime.now()
      credits = credits-1
      running = running + 1
      if running == config.total:
         print('ran out of coupons at ' + str(datetime.now()))
         exit()
   dists[index] = 0
   found = 0
   for i in range(0,len(users)):
      if users[i].state == 'n':
         found = 1
   if not found:
      credits = 0
#write to csv
filemanager.writecsv(filemanager.usersToArray(users), csvpath)

print(str(datetime.now()))
validation[0][0] = 'GOOD'
filemanager.writecsv(validation,valpath)
