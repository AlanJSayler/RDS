from datetime import datetime, timedelta
def init():
    global total
    global delay
    global expiry
    global fileName
    global seedEmail
    global fromName
    global message
    global userID
    global token
    global library
    global panel
    global survey1ID
    global survey1Questions
    global survey1Refs
    global survey2ID
    global survey2Questions
    global survey2Refs
    global suffix
    global allowOnlySuffixes
    global subject
    global subject2
    global fromWho
    global rootURL
    global version
    global form
    global version
    global basicURL
    global midURL
    global creditsForCompletions
    #users: edit the variables below this line
    #total specifies the total number of surveys that you will allow
    #the system to send out. A good number would be your budget/payment
    total = 100
    #delay specifies how long to wait before sennding a survey
    #delay of 1 day is standard for webRDS. Use 0 to test.
    delay = timedelta(days = 1)
    #expiry specifies the amount of time 
    #to wait before giving up on a participant
    expiry = timedelta(days = 7)
    #Specify a filename to store the state of the experiment
    #it'll be a csv, so probably throw a .csv on there
    fileName = ''
    #This is the email address of the first person
    #you want to send to. If you want to start multiple
    #threads, run this multiple times with different seeds, or manually edit the
    #csv file to stage new seeds.
    seedEmail = ''
    #Name that will show up on recipient's email client
    fromName = ''
    #Email address that the email containing the link will be sent from
    fromWho = ''
    #Message from your qualtrics message library to appear in the email invite
    message = ''
    #Your Qualtrics userID, it has a # in the middle
    userID = ''
    #Your Qualtrics token, find it on your qualtrics account information page
    token = ''
    #Qualtrics library in which your message, panel, and surveyIDs are stored,
    #find it on your qualtrics account information page
    library = '' 
    #Make a blank panel on qualtrics and put its ID here. You don't have to 
    #actually add anyone (not even seeds) to this panel. The system will
    #do that for you.
    panel = '' 
    #First survey ID, find it in your qualtrics library that you specified
    survey1ID = '' 
    #These are the questions in which the referrals are asked in Survey 1
    #Feel free to include as many or as few questions as you like
    survey1Questions = ['', '', '', '',  '', '']
    #I'm not sure why, but what questions qualtrics thinks it's returning
    #is different from what you ask for. The questions themselves are the 
    #same, Qualtrics just sends them numbered differently. You may want
    #to try the API call once with cURL or something. 
    #Getting this part right can be somewhat tricky and I haven't done 
    #a good job explaining it. Feel free to email me at asayler@wisc.edu
    #if you need some pointers
    survey1Refs = ['', '','','','','']
    survey2id =  '' 
    survey2questions = ['', '',  '',  '',  '', '']
    survey2refs = ['','','','','','']
    suffix = ''
    #1 to allow only emails with correct suffixes, 0 to allow any email, but with the suffix being the default
    allowOnlySuffixes = 1
    #This determines how many new surveys you send out for each completion
    #3 is the standard for webRDS. You may want to go as high as the number
    #of people that are being referred (that is to say, every referral should
    #get a survey)
    creditsForCompletions = 3
    #only edit this if you're using a different API version 
    for i in range(0,len(survey1questions)):
       survey2refs[i] = 'q' + survey2refs[i]
       survey1refs[i] = 'q' + survey1refs[i]
    #Default subject to send
    subject = ''
    #Subject to send just to seeds if altsubject is set
    subject2 = ''
    #Set to zero to just use subject, set to 1 if
    #you want the seeds to get subject2
    altSubject = 0
     

    #Users: you shouldn't have to edit anything below this line
    userID = userID.replace('#', '%23')
    subject = subject.replace(' ', '%20')
    subject2 = subject2.replace(' ', '%20')
    fromName = fromName.replace(' ', '%20') 
    rootURL = 'https://survey.qualtrics.com/WRAPI/ControlPanel/api.php' 
    version = '2.5'
    form = 'XML' 
    basicURL = rootURL + '?API_SELECT=ControlPanel&Version=' + version + '&Request=' 
    midURL = '&User=' + userID + '&Token=' + token + '&Format=' + form
    fromWho = fromWho.replace('@', '%40')
    
    return
