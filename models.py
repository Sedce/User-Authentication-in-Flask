from app import db
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Photos(Base, db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    trigger_type = db.Column(db.String(255), unique=True, nullable=True)
    photo_md5 = db.Column(db.String(32), unique=True, nullable=True)
    daylight = db.Column(db.SmallInteger, unique=True, nullable=True)
    longitude = db.Column(db.Numeric(10), unique=True, nullable=True)
    latitude = db.Column(db.Numeric(10), unique=True, nullable=True)
    bluetooth = db.Column(db.SmallInteger, unique=True, nullable=True)
    solar_battery_voltage = db.Column(db.Numeric(10), unique=True, nullable=True)
    backup_battery_voltage = db.Column(db.Numeric(10), unique=True, nullable=True)
    supply_5_voltage = db.Column(db.Numeric(10), unique=True, nullable=True)
    supply_4dot3_voltage = db.Column(db.Numeric(10), unique=True, nullable=True)
    supply_3dot3_voltage = db.Column(db.Numeric(10), unique=True, nullable=True)
    ioio_temperature = db.Column(db.Numeric(10), unique=True, nullable=True)
    cached_photo_count = db.Column(db.Integer(), unique=True, nullable=True)
    cell_data_used = db.Column(db.Integer(), unique=True, nullable=True)
    thumbnail_data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), unique=True, nullable=True)
    photo_data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), unique=True, nullable=True)
    album_id = db.Column(db.Integer(), unique=True, nullable=True)
    source_name = db.Column(db.Integer(), unique=True, nullable=True)
    date_taken = db.Column(db.DateTime, unique=True, nullable=True)
    HD1080p_data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), unique=True, nullable=True)

    def __repr(self):
        return '<Photos %s>' % self.username

class Camera_Parameters(Base, db.Model):
    __tablename__= "camera_parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_id = db.Column(db.Integer(), unique=True, nullable=True)
    source = db.Column(db.Integer(), unique=True, nullable=True)
    album = db.Column(db.Integer(), unique=True, nullable=True)
    timelapse = db.Column(db.Integer(), unique=True, nullable=True)

    def __repr__(self):
        return '<Camera_Parameters %i>' % self.camera_id


