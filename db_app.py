from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anoob09@localhost:3306/sputify'
db = SQLAlchemy(app)
class Users1(db.Model):
    userid = db.Column(db.String(30), primary_key=True)
    refreshtoken = db.Column(db.String(255), unique = True, nullable = False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(50))

