import os
from flask import Flask
from flask.ext.mail import Mail, Message
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "bdh931101@gmail.com"
app.config['MAIL_PASSWORD'] = "1Alzkdpf*^^*go"
app.config['MAIL_DEFAULT_SENDER'] = 'bdh931101@gmail.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_IMPORTS'] = ("app", )
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/wau'
# app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

# from app.controllers import request_async_crawl
# Initialize extensions
mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# Initialize Celery

celery.conf.update(app.config)

from app import controllers

db.create_all()