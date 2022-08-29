from email.policy import default
from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
import datetime



class Lot(db.Model):

    id = db.Column(db.Integer ,primary_key=True)
    destination = db.Column(db.String(100))
    plotid = db.Column(db.String(100))
    packhouse = db.Column(db.String(100))
    qty = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    packing = db.Column(db.Boolean)
    consignment = db.Column(db.Integer)
    lot_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    iecode = db.Column(db.String(100))
    companyname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    lot = db.relationship('Lot')
    message = db.relationship('Messages')
    consignment = db.relationship('Consignment')


class Messages(db.Model):

    id = db.Column(db.Integer ,primary_key=True)
    message = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Consignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    lot = db.Column(db.PickleType, db.ForeignKey('lot.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    consignment_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    pre = db.Column(db.Boolean)
    psc = db.Column(db.Boolean)