from flask import Flask, render_template, url_for, flash, redirect, Response,request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from src.form import RegistrationForm, LoginForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

#For video stream:
import cv2
from src.videoStream import VideoStream
from imageRecog import ImageRecog
import os


#For User login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap



app = Flask(__name__)
app.config['SECRET_KEY'] = 'c91b01cf28e66396744495723edd414e9ba3277b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loginCredentials.db'
app.config['SQLALCHEMY_BINDS'] = { 'CriminalDataBase':'sqlite:///CriminalDataBase.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

##-----------Login information
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#---------------------------------____Criminal DATABASE

class Criminal(db.Model):
    __bind_key__ = 'CriminalDataBase'
   # __tablename__ = 'criminals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    nationality = db.Column(db.String(80), nullable = False)
    years = db.Column(db.Integer, nullable = False)
    jail = db.Column(db.String(80), nullable = False)
    fileLocation = db.Column(db.String(80), nullable = False) #-----------------_For Image
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) #-------------------_Added

    crimes = db.relationship("Crime", backref="criminal")
    victim = db.relationship("Victim", backref="criminal")
    judge= db.relationship("Judge", backref = "criminal")

    def __init__(self, name, address, age, nationality, years, jail, fileLocation):
        self.name = name
        self.address = address
        self.age = age
        self.nationality = nationality
        self.years = years
        self.jail = jail
        self.fileLocation = fileLocation
    def __repr__(self):
        return f"<Criminal {self.name}>"

class Crime(db.Model):
    __bind_key__ = 'CriminalDataBase'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    crime_location = db.Column(db.String(80))
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable = False)

    def __init__(self, name , crime_location, criminal):
        self.name = name
        self.crime_location = crime_location
        self.criminal = criminal

    def __repr__(self):
        return f"<Crime {self.name}>"

class Victim(db.Model):
    __bind_key__ = 'CriminalDataBase'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    nationality = db.Column(db.String(80), nullable = True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable = False)

    def __init__(self, name, address, age, nationality, criminal ):
        self.name = name
        self.address = address
        self.age = age
        self.nationality = nationality
        self.criminal = criminal

    def __repr__(self):
        return f"<Victim {self.name}>"

class Judge(db.Model):
    __bind_key__ = 'CriminalDataBase'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    courtName = db.Column(db.String(80), nullable = False)
    courtLocation = db.Column(db.String(80), nullable = True)
    casesFought = db.Column(db.Integer, nullable = True)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable = False)

    def __init__(self, name, courtName, courtLocation , casesFought, criminal):
        self.name = name
        self.courtName = courtName
        self.courtLocation = courtLocation
        self.casesFought = casesFought
        self.criminal = criminal

    def __repr__(self):
        return f"<Judge {self.name}>"

#------------------------------------------>Display All Record

@app.route("/allrecord", methods = ['GET', 'POST'])
@login_required
def allrecord():
    if request.method == "POST":
        if request.form.get("Return"):
            return redirect(url_for("home"))
    return render_template("allrecord.html", criminalNameList = Criminal.query.all())



#---------------------------------------------->About Us
@app.route("/aboutus", methods = ['GET', 'POST'])
def aboutus():
    if request.method == "POST":
        if request.form.get("Return"):
            return redirect(url_for("home"))
    return render_template("about.html")
#------------------------------------------>Criminal Information display

@app.route("/informationDisplay", methods = ['GET', 'POST'])
@login_required
def informationDisplay():
    nameSubmitted = request.args.get('name')
    #nameSubmitted = "Sandesh Sitaula"
    criminalNameList = Criminal.query.filter_by(name = nameSubmitted).all()
    if request.method == 'POST':
        if request.form.get("Return"):
            return redirect(url_for('home'))

    additionalInformation = request.args.get('additionalInformation')

    if len(criminalNameList)==0:
        error = "Criminal record does not exist."
        return render_template("informationDisplay.html", error = error)

    elif additionalInformation == "victim":
        return render_template("informationDisplay.html", victim = criminalNameList )

    elif additionalInformation == "judge":
        return render_template("informationDisplay.html", judge = criminalNameList )

    elif additionalInformation == "crime":
        return render_template("informationDisplay.html", crime = criminalNameList )

    else:
        return render_template("informationDisplay.html", criminalNameList = criminalNameList)

    return render_template("informationDisplay.html")


#-------------------------------------------------------------------------------->Home

@app.route("/home", methods = ['GET', 'POST'])
@login_required
def home():

    ##For search by name---------------------->
    if request.method == "POST":
        if request.form.get("submitName"):
            nameSubmitted = request.form.get("search")

            return redirect(url_for("informationDisplay", name = nameSubmitted))


    #For search by Image------------------------>

    form = VideoStream()
    if form.validate_on_submit():
        global IpLink
        IpLink = form.link.data
        return redirect(url_for('video'))


    return render_template("home.html", title = "home", form = form)



#--------------------------------------------------------------->Login and Registration Part

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

#@login_manager.user_loader
#def load_user(user_id):
    #return User.query.get(int(user_id))
@app.route("/", methods = ['GET', 'POST'])
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            email = User.query.filter_by(email=form.email.data).first()
            if email:
                if check_password_hash(email.password, form.password.data):
                    login_user(email, remember=form.remember.data)
                    return redirect(url_for('home'))
                else:
                    flash("Password error.")
            else:
                flash("No matching email found.")

            # display flash message here

    return render_template('login.html', form=form)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been successfully created.', 'success')
            return redirect(url_for('login'))

        except IntegrityError:
            flash("User with this email address already exists.")
            db.session.rollback()
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('registration.html', form=form)

#------------------------------------------> Logout Part
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#-------------------------M--------------------->Delete
@app.route("/delete")
def delete():
    flash('Your account has been successfully deleted. Hope to see you again.', 'success')
    user = current_user.id
    User.query.filter(User.id == user).delete()
    db.session.commit()
    return redirect(url_for('login'))


#-------------------------Video Stream

def cam_frame():
    global camera
    if IpLink == '0':#-------------------------------------------------------->here work needs to done
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(IpLink) #----------------->>
    while True:
        success, frame = camera.read()
        if IpLink!='0':
            frame=cv2.transpose(frame)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route("/video", methods = ['POST','GET'])
@login_required
def video():
    if request.method == "POST":
        if request.form.get("Return"):
            camera.release()
            cv2.destroyAllWindows()
            return redirect(url_for('home'))

        elif request.form["submit_button"] == "Click":
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
            (nameCriminal , conf) = detect.detection()
            if conf==0:
                print("Nothing detected in Image.")
                return(redirect(url_for("informationDisplay", name = nameCriminal)))
            else:
                return(redirect(url_for("informationDisplay", name = nameCriminal)))
            return redirect(url_for("home"))

    return render_template('video.html')



@app.route("/videoFeed", methods = ['POST','GET'])
def videoFeed():
    return Response(cam_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')






if __name__ == "__main__":
    app.run(debug = True)
