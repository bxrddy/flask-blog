from flask import Flask, render_template, url_for
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
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login")
def login():

    form = LoginForm()
    return render_template('login.html', title = 'Login', form = form)


if __name__ == '__main__':
    app.run(debug = True)
