from flask import Flask, render_template, url_for, flash, redirect, Response,request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from src.form import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


#For video stream:
import cv2
from src.videoStream import VideoStream
from src.imageRecog import ImageRecog
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c91b01cf28e66396744495723edd414e9ba3277b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loginCredentials.db'
app.config['SQLALCHEMY_BINDS'] = { 'CriminalBaseSample':'sqlite:///CriminalBaseSample.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#-----------Login information
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#---------------------------------____Criminal DATABASE

class Criminal(db.Model):
    __bind_key__ = 'CriminalBaseSample'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    age=db.Column(db.Integer(), nullable = False)
    crimes = db.relationship("Crime", backref="criminal")


    def __init__(self, name, address, age):
        self.name = name
        self.address = address
        self.age = age

    def __repr__(self):
        return f"<Criminal {self.name}>"

#a criminal can have multiple crimes
class Crime(db.Model):
    __bind_key__ = 'CriminalBaseSample'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    crime_location = db.Column(db.String)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable = False)
    def __init__(self, name , crime_location, criminal):
        date_of_crime = datetime.date.today()
        self.name = name
        self.crime_location = crime_location
        self.criminal = criminal
    def __repr__(self):
        return f"<Crime {self.name}>"


#------------------------------------------>Home
@app.route("/informationDisplay", methods = ['GET', 'POST'])
def informationDisplay():
    nameSubmitted = request.args.get('name')
    criminalNameList = Criminal.query.filter_by(name = nameSubmitted).all()
    if request.method == 'POST':
        if request.form.get("Return"):
            return redirect(url_for('home'))

    if len(criminalNameList)==0:
        error = "Criminal record does not exist."
        return render_template("informationDisplay.html", error = error)
    else:
        return render_template("informationDisplay.html", criminalNameList = criminalNameList)

    return render_template("informationDisplay.html")


@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
#@login_required
def home():
    ##For search by name---------------------->
    if request.method == "POST":
        if request.form.get("submitName"):
            nameSubmitted = request.form.get("search")
            return redirect(url_for("informationDisplay", name = nameSubmitted))
                #print(f'name: {criminalNameList[0].name} \n address: {criminalNameList[0].address}')



    #For search by Image

    form = VideoStream()
    if form.validate_on_submit():
        print("----------------------->In")
        global IpLink
        IpLink = form.link.data
        return redirect(url_for('video'))


    return render_template("home.html", title = "home", form = form)






#------------------------------------------>Login and Registration Part

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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



#-------------------------Video Stream

def cam_frame():
    global camera
    camera = cv2.VideoCapture(0) #----------------->>
    while True:
        success, frame = camera.read()
        if not success:
            print("Device is not working properly.")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route("/video", methods = ["POST","GET"])
def video():
    if request.method == "POST":
        if request.form["submit_button"] == "Click":
            _, image = camera.read()

            #To check if the directory exists or not----------->

            forFolder = os.getcwd()
            newDirName = forFolder+'/ImageCaptured'
            if not (os.path.exists(newDirName)):
                os.mkdir(newDirName)
            #------------------------------->
            cv2.imwrite(newDirName+"/person.jpeg", image)
            #cv2.imwrite("/home/anju_chhetri/Desktop/TheCatch/ImageCaptured/person.jpeg", image)
            camera.release()
            cv2.destroyAllWindows()
            detect = ImageRecog(newDirName+"/person.jpeg")
            (name , conf) = detect.detection()
            if conf==0:
                print("Nothing detected in Image.")
            else:
                print(f"RESULT ------------------------> {name} conf: {conf}")



            return redirect(url_for("home"))

    return render_template('video.html')

@app.route("/videoFeed", methods = ["POST","GET"])
def videoFeed():

    return Response(cam_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug = True)
