from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer as Serializer
from app import db
from app.system_config import SysConfig


class User(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(64), unique=True, index=True, comment="用户名")
    NickName = db.Column(db.String(64), comment="用户昵称")
    PasswordHash = db.Column(db.String(128), comment="密码HASH值")
    RoleID = db.Column(db.Integer, db.ForeignKey('role.ID'), comment="外键-角色ID")

    @property
    def password(self):
        raise AttributeError('密码是不可读的属性！')

    @password.setter
    def password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.PasswordHash, password)

    # 通过用户信息来生成token，expiration是过期的时间，单位是秒
    # 这些认证信息是保存在内存的，项目重启就失效
    def generate_auth_token(self, expiration=600):
        s = Serializer(SysConfig.SecretKey(), expires_in=expiration)
        return s.dumps({'ID': self.ID})

    # 校验token
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SysConfig.SecretKey())
        try:
            data = s.loads(token)
        except SignatureExpired:
            print("token过期了")
            return SysConfig.ReturnCode("TOKEN_EXPIRED")
        except BadSignature:
            print("无效的token")
            return SysConfig.ReturnCode("TOKEN_ERROR")
        user = User.query.get(data['ID'])
        return user


class Role(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(64), unique=True, comment="角色名")
