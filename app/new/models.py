from app import db


class New(db.Model):
    __tablename__ = 'new'
    ID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Url = db.Column(db.String(500))
