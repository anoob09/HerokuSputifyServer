from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
class Users1(db.Model):
    userid = db.Column(db.String(30), primary_key=True)
    refreshtoken = db.Column(db.String(255), unique = True, nullable = False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(50))

