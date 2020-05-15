from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from db_app import db
from db_app import Users1

# test = Users1(userid = "anoob1", refreshtoken = "sjdf9832fiasda", latitude = 42.3243, longitude = 90.8348, city = "mumbai")
# db.create_all()
# db.session.add(test)
# db.session.commit()
users = Users1.query.filter_by(userid='anoob1').first()
print(users.userid)