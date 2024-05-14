from . import db
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(100))
    tag = db.Column(db.String(100))
    font = db.Column(db.String(100))
    font_size = db.Column(db.Integer)
    align = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_token(self):
        serial = Serializer(current_app.config['SECRET_KEY'])
        return serial.dumps({'doc_id':self.id}, salt='share')
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(current_app.config['SECRET_KEY'])
        try:
            print("Attempting loads")
            doc_id = serial.loads(token, salt='share', max_age=300)['doc_id']
            print("Did loads")
        except:
                return None
        return Document.query.get(doc_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    documents = db.relationship('Document')

    def get_token(self):
        serial = Serializer(current_app.config['SECRET_KEY'])
        return serial.dumps({'user_id':self.id}, salt='reset_password')
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(current_app.config['SECRET_KEY'])
        try:
            print("Attempting loads")
            user_id = serial.loads(token, salt='reset_password', max_age=300)['user_id']
            print("Did loads")
        except:
                return None
        return User.query.get(user_id)