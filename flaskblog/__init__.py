from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

'''
- The 'SECRET_KEY' can be any random string
- Corey Schafer (YouTuber) suggests the below method for beginners:
    1. Open the python interpreter
    2. Execute the following to get the random string
                import secrets
                secrets.token_hex(16)

       OUTPUT:  <RANDOM_STRING_OF_16_CHARACTERS_WILL_BE_YOUR_OUTPUT>
'''
app.config['SECRET_KEY'] = '774fe35b1314db2573faee216d9e6758'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating the instance of the database
db = SQLAlchemy(app)

# Creating the instance of the Bcrypt class
bcrypt = Bcrypt(app)

# Creating the instance of the LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes