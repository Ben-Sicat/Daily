# this is where the flask app will reside

from flask import Flask 
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

#.... imports from other modules (data_service, etc)
#.... routes for the app

if __name__ == '__main__':
    app.run(debug=True)