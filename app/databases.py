from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class raceInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) # レース名
    date = db.Column(db.String(10))  # 日付
    week = db.Column(db.String(1))   # 曜日
    prefecture = db.Column(db.String(4)) # 都道府県
    city = db.Column(db.String(8)) # 市町村
    distance = db.Column(db.Integer) # 距離
    gain = db.Column(db.Integer) # 獲得標高
    url = db.Column(db.String(100)) # URL
