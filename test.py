from flask import Flask
from flask import render_template, url_for, flash, redirect, Response,request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =   'sqlite:///ImageTest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'c91b01cf28e66396744495723edd414e9ba3277b'
folder = "CriminalImage"
class Criminal(db.Model):
   # __tablename__ = 'criminals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    fileLocation = db.Column(db.String(80), nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) #-------------------_Added
#{{ date_of_something.strftime('%Y-%m-%d') }}


    def __init__(self, name, fileLocation):
        self.name = name
        self.fileLocation = fileLocation
@app.route("/")
def home():
    return render_template("test.html", criminalNameList = Criminal.query.all())

if __name__ == "__main__":
    app.run(debug = True)
