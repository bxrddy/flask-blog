import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

''' 
### Dummy Posts ###
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
'''

@app.route("/")
@app.route("/home")
def home():

    # Get the page number from the URL. Default is set to first page
    page    =  request.args.get('page', 1, type = int)

    # Goes to that specific page and only displays five posts per page
    posts   =  Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)

    return render_template('home.html', posts = posts)


@app.route("/about")
def about():
    return render_template('about.html', title = 'About')


@app.route("/register", methods = ['GET', 'POST'])
def register():

    # If user is already logged in then redirect the user to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        # decode('utf-8') is used to convert the hashed password from byte to string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You can now login!", "success")   # Used the Bootstrap 'success' class as a category for flash
        return redirect(url_for('login'))

    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():

    # If user is already logged in then redirect the user to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)

            # Stores the information of the URL user tried to access before authentication
            next_page = request.args.get('next')

            # Redirects the user to the desired URL after authentication
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login failed. Please check your credentials!", "danger")

    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You are now logged out!", "warning")
    return redirect(url_for('home'))


def save_picture(form_picture):

    # Renaming the image file
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext

    # Getting the absolute path so that we can save the image in that location
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    # Resizing the image
    output_size = (200, 200)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_filename


@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username   =  form.username.data
        current_user.email      =  form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':

        # Used to populate user's information in the form
        form.username.data  =  current_user.username
        form.email.data     =  current_user.email

    image_file = url_for('static', filename = f"profile_pics/{ current_user.image_file }")
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)


@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()

    if form.validate_on_submit():

        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


@app.route("/post/<int:post_id>")
def post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title = post.title, post = post)


@app.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id = post.id))

    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'info')

    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):

    # Get the page number from the URL. Default is set to first page
    page    =  request.args.get('page', 1, type = int)

    user    =  User.query.filter_by(username = username).first_or_404()

    # Goes to that specific page and only displays five posts per page
    posts   =  Post.query\
                        .filter_by(author = user)\
                        .order_by(Post.date_posted.desc())\
                        .paginate(page = page, per_page = 5)

    return render_template('user_posts.html', posts = posts, user = user) 
