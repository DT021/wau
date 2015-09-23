# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app import app

class MapInfo(db.Model):
    __tablename__ = 'mapinfo'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(240))
    result_all = db.Column(db.Text)

    def __init__(self, url, result_all):
        self.url = url
        self.result_all = result_all

    def __repr__(self):
        return '<id {}>'.format(self.id)

class GeoInfo(db.Model):
	__tablename__ = "geoinfo"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	latitude = db.Column(db.Float, index=True)
	longitude = db.Column(db.Float, index=True)
	name = db.Column(db.String(128))
	address = db.Column(db.String(128))
	roadAddr = db.Column(db.String(128))
	description = db.Column(db.Text)
	phone = db.Column(db.String(128))
	category1 = db.Column(db.String(64))
	category2 = db.Column(db.String(64))
	homepage = db.Column(db.String(128))
	subwayID = db.Column(db.Integer)
	bizhour = db.Column(db.String(128))

	def __init__(self, **kwargs):
		super(GeoInfo, self).__init__(**kwargs)

	def __repr__(self):
		return '<id {}>'.format(self.id)

