from flask import Flask, render_template, url_for, flash, redirect, Response,request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from Form.form import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c91b01cf28e66396744495723edd414e9ba3277b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loginCredentials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#-----------Login information
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#------------------------------------------>Login and Registration Part

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.form.get("submitName"):
            name = request.form.get("search")
            print(f'nameeeeeeeeee------       {name}')
            #return redirect(url_for('login'))
    return render_template("searchInput.html")


@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            if check_password_hash(email.password, form.password.data):
                login_user(email, remember=form.remember.data)
                #return '<h1> Sucess</h1>'#---------------put home page here
                return redirect(url_for('home'))
        return '<h1>Invalid username or password</h1>' # display flash message here
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

#@login_required
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


if __name__ == "__main__":
    app.run(debug = True)
