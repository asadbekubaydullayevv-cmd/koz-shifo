from app import db
from datetime import datetime

class Shifokor(db.Model):
    __tablename__ = 'shifokorlar'
    id = db.Column(db.Integer, primary_key=True)
    ism = db.Column(db.String(100), nullable=False)
    mutaxassislik = db.Column(db.String(100))
    telefon = db.Column(db.String(20))
    tashqi = db.Column(db.Boolean, default=False)
    bonus_foiz = db.Column(db.Float, default=0)
    faol = db.Column(db.Boolean, default=True)
    yaratilgan = db.Column(db.DateTime, default=datetime.utcnow)

class Xizmat(db.Model):
    __tablename__ = 'xizmatlar'
    id = db.Column(db.Integer, primary_key=True)
    nomi = db.Column(db.String(100), nullable=False)
    narxi = db.Column(db.Float, nullable=False)
    kategoriya = db.Column(db.String(50))
    faol = db.Column(db.Boolean, default=True)

class Bemor(db.Model):
    __tablename__ = 'bemorlar'
    id = db.Column(db.Integer, primary_key=True)
    ism = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20))
    tug_sana = db.Column(db.Date)
    yaratilgan = db.Column(db.DateTime, default=datetime.utcnow)

class Qabul(db.Model):
    __tablename__ = 'qabullar'
    id = db.Column(db.Integer, primary_key=True)
    bemor_id = db.Column(db.Integer, db.ForeignKey('bemorlar.id'))
    shifokor_id = db.Column(db.Integer, db.ForeignKey('shifokorlar.id'))
    xizmat_id = db.Column(db.Integer, db.ForeignKey('xizmatlar.id'))
    summa = db.Column(db.Float, nullable=False)
    tolov_turi = db.Column(db.String(20))
    sana = db.Column(db.DateTime, default=datetime.utcnow)
    izoh = db.Column(db.String(200))
    bemor = db.relationship('Bemor', backref='qabullar')
    shifokor = db.relationship('Shifokor', backref='qabullar')
    xizmat = db.relationship('Xizmat', backref='qabullar')

class Xarajat(db.Model):
    __tablename__ = 'xarajatlar'
    id = db.Column(db.Integer, primary_key=True)
    nomi = db.Column(db.String(100), nullable=False)
    summa = db.Column(db.Float, nullable=False)
    kategoriya = db.Column(db.String(50))
    sana = db.Column(db.DateTime, default=datetime.utcnow)
    izoh = db.Column(db.String(200))

class Smena(db.Model):
    __tablename__ = 'smenalar'
    id = db.Column(db.Integer, primary_key=True)
    sana = db.Column(db.Date, nullable=False, unique=True)
    naqd_tushum = db.Column(db.Float, default=0)
    terminal_tushum = db.Column(db.Float, default=0)
    aralash_tushum = db.Column(db.Float, default=0)
    jami_tushum = db.Column(db.Float, default=0)
    bemorlar_soni = db.Column(db.Integer, default=0)
    izoh = db.Column(db.String(300))
    yopilgan = db.Column(db.Boolean, default=False)
    yopilgan_vaqt = db.Column(db.DateTime)

class TashqiShifokorXarajat(db.Model):
    __tablename__ = 'tashqi_shifokor_xarajatlar'
    id = db.Column(db.Integer, primary_key=True)
    shifokor_id = db.Column(db.Integer, db.ForeignKey('shifokorlar.id'))
    sana = db.Column(db.Date, nullable=False)
    operatsiyalar_soni = db.Column(db.Integer, default=0)
    operatsiya_tushum = db.Column(db.Float, default=0)
    yol_haqi = db.Column(db.Float, default=0)
    yashash = db.Column(db.Float, default=0)
    ovqatlanish = db.Column(db.Float, default=0)
    xizmat_haqi = db.Column(db.Float, default=0)
    bonus_foiz = db.Column(db.Float, default=0)
    bonus_summa = db.Column(db.Float, default=0)
    jami_xarajat = db.Column(db.Float, default=0)
    izoh = db.Column(db.String(300))
    yaratilgan = db.Column(db.DateTime, default=datetime.utcnow)
    shifokor = db.relationship('Shifokor', backref='tashqi_xarajatlar')
