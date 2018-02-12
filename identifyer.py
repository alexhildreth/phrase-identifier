import pymongo
from pymongo import *

client = MongoClient()
mongo = MongoClient('localhost', 27017)
db = mongo['testdb']
coll = db['testcoll']

'''this worked
db.testcoll.insert(
    {'word': 'word1', 
     'nextWord': 'nextWord1'
    }
)'''

'''this worked
word = 'word2'
nextW = 'nextWord2'
db.testcoll.insert(
    {'word': word, 
     'nextWord': nextW
    }
)'''

'''this worked
word = 'word3'
nextW = 'nextWord3'
db.testcoll.insert(
    {'word': word, 
     'nextWord': {nextW : 1}
    }
)'''

'''this worked
word = 'word4'
db.testcoll.insert(
        {'word': word,
         'nextWords': {}
        }
    )'''

'''w = 'your'
next_word = 'social'
db.testcoll.update(
        {'word': w},
        {'$inc': {'nextWords.' + next_word : 1}}
    )'''

'''this worked
word = 'word1'
if db.testcoll.find({'word': word}).count() > 0:
    print('True')
else:
    print('False')'''

'''this worked
word = 'word3'
next_word = 'nextWord3'
if db.testcoll.find({'word': word, 'nextWord.'+ next_word : {'$exists':True} }).count() > 0:
    print('True')
else:
    print('False')'''
