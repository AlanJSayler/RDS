# RDS

This is a short project to allow researcers to execute a webRDS research with a set of Qualtrics surveys. This means sending out a survey to a seed email address, and that person refers others to take the survey as well, and the survey propogates forward like that. This script is to simply interact with Qualtrics' API to automatically send out the new surveys as current participants complete their surveys. 

#Usage

Copy all the files into a directory, fill in the configuration file (there are comments to help you through this), and set up a cron job to run rds.sh repeatedly. You will need to know things about your Qualtrics survey, such as the message ID, survey ID, your token, and so on.

Email me at asayler@wisc.edu if you have questions or problems running.

#History

I made this project to run a peer's webRDS research project in 2015-2016. 

