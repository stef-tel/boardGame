from . import db
from flask_login import UserMixin
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    numberConnection = db.Column(db.Integer)
    lastActivity = db.Column(db.DateTime)
    lastDisconnect = db.Column(db.DateTime)

    @hybrid_property
    def connectionStatus(self):
        if self.numberConnection != None :
            if self.numberConnection > 0 :
                status = "Connected" 
            else :
                status = "Disconnected"
        else:
           status = "Disconnected" 
        return status
        

    def __repr__(self):
        return '<User %r>' % self.username

class Connection(db.Model):
    __tablename__ = 'connection'
    dateTime = db.Column(db.DateTime, primary_key=True) # primary keys are required by SQLAlchemy
    player_id = db.Column(db.Integer, ForeignKey("user.id"), primary_key=True)
    status = db.Column(db.String(5))

    player = relationship("User")
