#This file contains the functions necessary to interact with qualtrics' API
#I fully recognize that the correct way is to pass the arguments with JSON
#but as of August 2015, the Qualtrics API v2.5 did not allow that. 
#I also realize that I probably should have made a URL builder function,
#that allows for users to use whatever arguments they want or didn't.
#I plan to rewrite when I have more time.

import config
import urllib.request
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
#make the request with the given url
def makeRequest (url):
    response = urllib.request.urlopen(url)
    lines = bytes.decode(response.read())
    return lines

#add a recipient to a qualtrics panel
#this step has to be done, but isn't really interesting since we're just using
#one panel
def addRecipient (emailaddress):
    e = emailaddress.replace('@', '%40')
    url = (config.basicurl + 'addRecipient' + config.midurl + '&LibraryID=' +
          config.library + '&PanelID=' + config.panel + '&Email=' + e)
    return url
#send a survey to an individual without worrying about the 
#subject line or expiration
def sendSurveyToIndividual (recipient, survey):
    url =(config.basicurl + 'sendSurveyToIndividual' + config.midurl + 
         '&SurveyID=' + survey + '&SendDate=2015-01-01%2000%3A00%3A00&FromEmail='
         + config.fromwho + '&FromName=' + config.fromname + '&Subject=' + 
         config.subject + '&MessageID=' + config.message + '&MessageLibraryID=' 
         + config.library + '&PanelID=' + config.panel + '&PanelLibraryID=' + 
         config.library + '&RecipientID=' + recipient + 
         '&ExpirationDate=2017-01-01%2000%3A00%3A00')
    return url

#send a survey to an individual with the subject and expiry line
def sendSurveyToIndividualSubjectExpiry (recipient, survey, subject):
    expirydatetime = datetime.now() + config.expiry
    expirystring = expirydatetime.strftime('%Y-%m-%d %H:%M:%S')
    expirystring = expirystring.replace(' ', '%20' )
    expirystring = expirystring.replace(':', '%3A')
    url = (config.basicurl + 'sendSurveyToIndividual' + config.midurl + 
          '&SurveyID=' + survey + 
          '&SendDate=2015-01-01%2000%3A00%3A00&FromEmail=' + 
          config.fromwho + '&FromName=' + config.fromname + '&Subject=' + 
          subject + '&MessageID=' + config.message + '&MessageLibraryID=' 
          + config.library + '&PanelID=' + config.panel + '&PanelLibraryID=' 
          + config.library + '&RecipientID=' + recipient + '&ExpirationDate=' 
          + expirystring)
    print(expirystring)
    return url 
#TODO change this to allow for different numbers of responses
#get the data about a survey from qualtrics
def getLegacyResponseDataOfIndividual (recipientID, surveyID, quests):
    url = (config.basicurl + 'getLegacyResponseData' + config.midurl + 
          '&SurveyID=' + surveyID + '&ResponseID=' + recipientID+ 
          '&Questions=QID' + quests[0] + '%2CQID' + quests[1] + '%2CQID' + 
          quests[2] + '%2CQID' + quests[3] + '%2CQID' + quests[4])
    return url
#Updated version of above method to allow for different numbers of responses
def getLegacyResponseData (surveyID, quests):
    q = quests[0]
    for i in range(1,len(quests)):
        q = q + '%2CQID' + quests[i]
    url = (config.basicurl + 'getLegacyResponseData' + config.midurl + 
          '&SurveyID=' + surveyID + '&Questions=QID' + q) 
    return url

#Send a survey by adding a recipient to a panel, and then send it
def sendSurvey (emailaddress, survey):
    xml  = makeRequest(addRecipient(emailaddress))
    y  = BeautifulSoup(xml, "lxml")
    thestring = str(y.html.body.xml.result.recipientid.string)
    print(sendSurveyToIndividual(thestring,survey))
    response =  makeRequest(sendSurveyToIndividual(thestring, survey))
    return response

#same as above, but uses the subject and expiration
def sendSurveySubjectExpiry (emailaddress, survey, subject):
    xml  = makeRequest(addRecipient(emailaddress))
    y  = BeautifulSoup(xml, "lxml")
    thestring = str(y.html.body.xml.result.recipientid.string)
    response =  makeRequest(sendSurveyToIndividualSubjectExpiry(thestring, survey,subject))
    return response



