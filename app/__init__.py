from flask import Flask
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
# 导入flask_restful需要的包
from flask_restful import Api, Resource
# 引入marshmallow的包
from flask_marshmallow import Marshmallow


# 实例化数据库对象
db = SQLAlchemy()
# 实例化marshmallow
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:AliCentOSMysql123456@localhost:3306/FlaskRESTFul'
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

    from app.user import user as user_bp
    app.register_blueprint(user_bp)

    from app.article import article as articler_bp
    app.register_blueprint(articler_bp)

    from app.article.resource import ArticleResource, ArticleSingleResource
    api.add_resource(ArticleResource, '/article')
    api.add_resource(ArticleSingleResource, '/article/single')

    from app.user.resource import UserResource
    api.add_resource(UserResource, '/user')

    from app.user.resource import LoginResource
    api.add_resource(LoginResource, '/login')

    from app.user.resource import CheckToken
    api.add_resource(CheckToken, '/token')

    return app
