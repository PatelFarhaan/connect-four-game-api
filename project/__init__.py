#<==================================================================================================>
#                                          IMPORTS
#<==================================================================================================>
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine


#<==================================================================================================>
#                                          CONFIG
#<==================================================================================================>
app = Flask(__name__)
database_string = "mongodb://admin:admin@database:27017/admin"
app.config['SECRET_KEY'] = '***REMOVED***'
connection_string = {
    "host": database_string
}
app.config['MONGODB_SETTINGS'] = connection_string
db = MongoEngine(app)
ma = Marshmallow(app)


#<==================================================================================================>
#                                         BLUEPRINT
#<==================================================================================================>
from project.apis.views import api_blueprint

app.register_blueprint(api_blueprint)
