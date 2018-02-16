'''''''''''''''''''''''''''''''''''''''''''''
Word Counter by Alex Hildreth
v0.3
Using the PRAW Reddit API wrapper and MongoDB,
this script pulls comments from the Reddit
/all stream and parses all individual words,
storing them in a DB document that contains
a map of all other words that have come after 
the word, along with a count of how many times
the next word has occured.

This data may be used in conjuction with data
from string_parser.py to identify memes or
phrases.

MongoDB note - the database should have an
ascending index on the "word" field
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


#pull comments from Reddit's /r/all stream, parse them, and add to/update the database
def commentParser():
    commentCount = 1
    for comment in r.subreddit('all').stream.comments():
        db.wordbucket.update({}, {'$inc': {'commentCount' : 1}}) #increase the comment count

        comment_body = sanitize_input(comment.body) #sanitize the input and split into individual words
        comment_body = comment_body.split()  
        
        position = 0
        for word in comment_body: 
            if not check_db(word): #add current word to main dict if not already in there
                add_word(word) 
        
            if position < len(comment_body) - 1: #if not last word in comment, add/update next word in database
                update_next(word, comment_body[position+1])

            position += 1

        #print to log to confirm functionality
        if commentCount % 20 == 0:
            print("Parsing comment pull... " + str(commentCount))

        commentCount += 1


#removes all non-alphanumeric characters from the comment and casts to lower
def sanitize_input(x):
    s = re.sub('[^0-9a-zA-Z ]+', '', str(x))
    return s.lower()


#checks the db for a word
def check_db(word):
    if db.wordbucket.find({'word': word}).count() > 0:
        return True
    else:
        return False


#updates the count of the next word. Will add the word if not there.
def update_next(w, next_word):
    db.wordbucket.update(
        {'word': w},
        {'$inc': {'nextWords.' + next_word : 1}}
    )


#adds a word to the db
def add_word(word):
    db.wordbucket.insert(
        {'word': word,
         'nextWords': {}
        }
    )