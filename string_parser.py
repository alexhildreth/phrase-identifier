'''''''''''''''''''''''''''''''''''''''''''''
Phrase Identifyer by Alex Hildreth
v0.5
Using the PRAW Reddit API wrapper and MongoDB,
this script pulls comments from the Reddit
/all stream and parses short phrases between
2 and 8 words. Each potential phrase is logged
in a Mongo database with an updated frequency
counter. The data is intended to be used with
a front-end system where a user can mark 
potential phrases as a full phrase, a meme, or 
a part of a meme or phrase. That data would then
be used to help the system identify phrases
on its own and identify newly emerging meme
phrases.

MongoDB note - the database should have an
ascending index on the "phrase" field
'''''''''''''''''''''''''''''''''''''''''''''

import pymongo
from pymongo import *
import praw
import re
from secrets import LoginInfo


#Reddit log in to user agent
login = LoginInfo()
r = praw.Reddit(client_id=login.getID(),
                     client_secret=login.getSecret(), password=login.getPassword(),
                     user_agent=login.getAgent(), username=login.getUsername())


#initialize database connection
client = MongoClient()
mongo = MongoClient('localhost', 27017)
db = mongo['phrasedb']


#parses comments and calls update_db()
def stringParser():
    commentCount = 1
    for comment in r.subreddit('all').stream.comments():
        db.phrasebucket.update({}, {'$inc': {'commentCount' : 1}}) #increase the comment count
        commentCount += 1

        comment_body = sanitize_input(comment.body) #sanitize the input and split into individual words
        comment_body = comment_body.split()

        if checkPassConditions(comment_body): #check for pass conditions
            continue       

        position = 0
        for word in comment_body: 
            if position < len(comment_body) - 1:
                currentPhrase = word
                for i in range(len(comment_body) - position - 1):
                    if i >= 7: #limit phrases to 8 or less words
                        break
                    currentPhrase += " " #continue to concatenate phrase
                    currentPhrase += comment_body[position + i + 1]
                    update_db(currentPhrase)
                                       
            position += 1

        #print to log to confirm functionality
        if commentCount % 20 == 0:
            print("Parsing comment pull... " + str(commentCount))


#removes all non-alphanumeric characters from the comment and casts to lower
def sanitize_input(x):
    s = re.sub('[^0-9a-zA-Z ]+', '', str(x))
    return s.lower()


#checks the db for a phrase and updates
def update_db(phrase):
    if db.phrasebucket.find({'phrase': phrase}).count() > 0:
        db.phrasebucket.update(
            {'phrase': phrase},
            {'$inc': {'count' : 1}}
        )
    else:
        phraseArr = phrase.split()
        length = len(phraseArr)
        db.phrasebucket.insert(
            {'phrase': phrase,
            'count': 1,
            'length': length
            }
        )


#checks comment arrays for pass conditions 
def checkPassConditions(comment_body):
    for x in comment_body:
        if len(x) > 15:
            return True   
    if len(comment_body) > 12: 
        return True
    elif 'bot' in comment_body: 
        return True
    else:
        return False