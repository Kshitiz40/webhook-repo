from flask_pymongo import PyMongo

# Setup MongoDB here
# mongo = PyMongo(uri="mongodb://localhost:27017/database")
mongo = PyMongo() #Link mongoDB later in create_app with app config