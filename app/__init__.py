from flask import Flask
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
# 导入flask_restful需要的包
from flask_restful import Api, Resource
# 引入marshmallow的包
from flask_marshmallow import Marshmallow
# 导入flask-redis
from flask_redis import FlaskRedis


# 实例化数据库对象
db = SQLAlchemy()
# 实例化marshmallow
ma = Marshmallow()
# 实例化flask-redis
redis_client = FlaskRedis()
# docker: flask-mysql
# mysql_connet_string = "flask-mysql"
# 下面是使用本地，也就是venv这种类型的连接地址
mysql_connet_string = "localhost"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:AliCentOSMysql123456@{mysql_connet_string}:3306/FlaskRESTFul"
    # 添加flask-reids的配置
    # app.config['REDIS_URL'] = "redis://localhost:6379/0"
    # 关闭数据追踪，避免内存资源浪费
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 解决跨域问题
    CORS(app, supports_credentials=True)
    # 是否显示执行的sql语句
    # app.config['SQLALCHEMY_ECHO'] = True
    db = SQLAlchemy(app)
    # 将app中的配置文件应用到db中
    db.init_app(app)
    # 将app中的配置文件应用到api中
    api = Api(app)
    # 将app中的配置文件应用到marshmallow中
    ma.init_app(app)
    # 将app中的配置文件应用到flask-redis中
    redis_client.init_app(app)

    from app.user import user as user_bp
    app.register_blueprint(user_bp)

    from app.article import article as articler_bp
    app.register_blueprint(articler_bp)

    from app.new import new as new_bp
    app.register_blueprint(new_bp)
    # === 上面是注册蓝图 ===
    from app.new.resource import NewResource
    api.add_resource(NewResource, '/new')

    from app.article.resource import ArticleResource, ArticleListResource
    api.add_resource(ArticleResource, '/article')
    api.add_resource(ArticleListResource, '/article_list')

    from app.user.resource import UserResource
    api.add_resource(UserResource, '/user')

    from app.user.resource import LoginResource
    api.add_resource(LoginResource, '/login')

    from app.user.resource import CheckToken
    api.add_resource(CheckToken, '/token')

    from app.gbcomment.resource import GBComment
    api.add_resource(GBComment, '/gb_comment')

    return app


# 创建项目的时候初始化表内数据的函数
def init_func():
    from app.user.models import Role, User
    role = Role(RoleName="管理员")
    db.session.add(role)
    db.session.commit()
    user = User(UserName="admin", password="123456", RoleID=role.ID)
    db.session.add(user)
    db.session.commit()
    role = Role(RoleName="用户")
    db.session.add(role)
    db.session.commit()
