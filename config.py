from flask_pymongo import PyMongo

# mongo = None

def init_mongo(app):
    global mongo
    mongo = PyMongo(app)
    return mongo