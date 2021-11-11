from flask import Flask
from .main.routes import main
from .db_conf import mongo

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = "mongodb+srv://ddsds:ows5HCSFyki3TnjA@cluster0.wtfwc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    mongo.init_app(app)
    app.register_blueprint(main)
    return app
