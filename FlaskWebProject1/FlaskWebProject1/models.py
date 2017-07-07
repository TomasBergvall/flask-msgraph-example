#from flask import Flask
from sqlalchemy import DDL, event
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from FlaskWebProject1 import app, lm

db = SQLAlchemy(app)

# SQLAlchemy classes that reference to tables
# user_pofile, status, async_operation
class UserProfile(UserMixin, db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(64), nullable=False)
    external_authorizer = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    __table_args__ = (db.UniqueConstraint('external_id', 'external_authorizer', name='authorizer_id'), )

class WebApplication(UserMixin, db.Model):
    __tablename__ = 'web_application'
    web_application_id = db.Column(db.Integer, primary_key=True)
    web_application_name = db.Column(db.String(64), nullable=False)

class AccessControl(UserMixin, db.Model):
    __tablename__ = 'access_control'
    user_id = db.Column(db.Integer, db.ForeignKey(UserProfile.id))
    web_application_id = db.Column(db.Integer, db.ForeignKey(WebApplication.web_application_id))
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'web_application_id', name='pk_AccessControl'), )


event.listen(
        WebApplication.__table__, 'after_create',
        DDL(
                """ INSERT INTO web_application (web_application_name) VALUES('flask-msgraph-example'); """)
)

if __name__ == '__main__':
    db.create_all()
    