from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    passw = db.Column(db.String(150))
    reg_date = db.Column(db.DateTime(timezone=True), default=func.now())
    expense = db.relationship('Expense')


class Expense(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150))
    paidto = db.Column(db.String(150))
    amount = db.Column(db.Integer)
    mon = db.Column(db.String(150))
    status = db.Column(db.String(150))
    transaction_date = db.Column(db.String(100))
    prev_bal = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
