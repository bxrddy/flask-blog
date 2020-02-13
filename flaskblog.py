from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

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


### Creating the Models ###

# User Model
class User(db.Model):

    id          =  db.Column(db.Integer, primary_key = True)
    username    =  db.Column(db.String(20), nullable = False, unique = True)
    email       =  db.Column(db.String(120), nullable = False, unique = True)
    image_file  =  db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password    =  db.Column(db.String(60), nullable = False)

    # Establishing realtionship between the 'User' and 'Post' Models
    posts       =  db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Post Model
class Post(db.Model):

    id           =  db.Column(db.Integer, primary_key = True)
    title        =  db.Column(db.String(100), nullable = False)
    date_posted  =  db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content      =  db.Column(db.Text, nullable = False)

    user_id      =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    },
    {
        'author': 'Brijesh Reddy',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'April 22, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)


@app.route("/about")
def about():
    return render_template('about.html', title = 'About')


@app.route("/register", methods = ['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")   # Used the Bootstrap 'success' class as a category for flash
        return redirect(url_for('home'))

    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'abc@gmail.com' and form.password.data == '123':
            flash(f"You are now logged in!", "success")   # Used the Bootstrap 'success' class as a category for flash
            return redirect(url_for('home'))
        else:
            flash(f"Login failed. Please check your credentials!", "danger")

    return render_template('login.html', title = 'Login', form = form)


if __name__ == '__main__':
    app.run(debug = True)
