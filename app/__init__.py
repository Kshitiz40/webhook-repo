from flask import Flask
from flask_cors import CORS
from app.extensions import mongo
from app.webhook.routes import webhook
import os
from dotenv import load_dotenv

load_dotenv()

# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # Configure MongoDB URI
    # app.config["MONGO_URI"] = "mongodb://localhost:27017/GithubActions" # Local MongoDB
    app.config["MONGO_URI"] = os.getenv("MONGO_URI") # MongoDB Atlas
    
    CORS(app)
    mongo.init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
