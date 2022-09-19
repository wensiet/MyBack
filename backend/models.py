from backend import db, manager
from pydantic import BaseModel
from datetime import datetime
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_user = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User %r>' % self.id


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


class GetUser(BaseModel):
    username: str
    password: str


@manager.user_loader
def load_user(id):
    return Users.query.get(id)
