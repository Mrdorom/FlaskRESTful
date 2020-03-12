from app import db


class Article(db.Model):
    __tablename__ = 'article'
    ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.ID'))
    Title = db.Column(db.String(50))
    Text = db.Column(db.Text())
