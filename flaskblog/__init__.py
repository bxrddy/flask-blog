from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

from flaskblog import routes