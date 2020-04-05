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


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:AliCentOSMysql123456@localhost:3306/FlaskRESTFul'
    # 添加flask-reids的配置
    app.config['REDIS_URL'] = "redis://localhost:6379/0"
    # 添加Celery的配置，与上面这个的库最好分开（/0）-这里不使用
    app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
    app.config['CELERY_BACKEND_URL'] = "redis://localhost:6379/1"

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
    # 将app中的配置文件应用到flask-redis中--暂时不使用
    # 等后面celery接入进来后用于读取celery异步获取的信息
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

    return app
