from app import db


class Article(db.Model):
    __tablename__ = 'article'
    ID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.ID'), comment="外键-用户ID")
    CreateDay = db.Column(db.Date, comment="文章创建日期")
    CreateTime = db.Column(db.DateTime, comment="文章发布时间")
    UpdateTime = db.Column(db.DateTime, comment="文章修改时间")
    Title = db.Column(db.String(50), comment="文章标题")
    Text = db.Column(db.Text(), comment="文章内容")
