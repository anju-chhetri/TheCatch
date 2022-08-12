from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =   'sqlite:///CriminalDataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'c91b01cf28e66396744495723edd414e9ba3277b'


class Criminal(db.Model):
   # __tablename__ = 'criminals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
    nationality = db.Column(db.String(80), nullable = False)
    years = db.Column(db.String(80), nullable = False)

    crimes = db.relationship("Crime", backref="criminal")
    victim = db.relationship("Victim", backref="criminal")
    judge= db.relationship("Judge", backref = "criminal")

    def __init__(self, name, address, age, nationality, years):
        self.name = name
        self.address = address
        self.age = age
        self.nationality = nationality
        self.years = years
    def __repr__(self):
        return f"<Criminal {self.name}>"

class Crime(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    #date_of_crime = db.Column(db.Date)
    crime_location = db.Column(db.String)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable = False)

    def __init__(self, name , crime_location, criminal):
        self.name = name
        self.crime_location = crime_location
        self.criminal = criminal

    def __repr__(self):
        return f"<Crime {self.name}>"

class Victim(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(80), nullable = False)
    country = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable = False)

    def __init__(self, name, address, age, country, criminal):
        self.name = name
        self.address = address
        self.age = age
        self.country = country
        self.criminal = criminal

    def __repr__(self):
        return f"<Judge {self.name}>"

#@app.route("/", methods = ['GET', 'POST'])
#@app.route("/home", methods = ['GET', 'POST'])
#def home():
    #return render_template('home.html', title = "home", form= form, criminal = Criminal.query.all())



#if __name__ == "__main__":
    #app.run(debug = True)
