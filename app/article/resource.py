from flask_restful import Resource, reqparse
from datetime import datetime

from app import db
from app.user.models import User
from app.auth import token_required, admin_required
from app.system_config import SysConfig
from .models import Article
from .schema import ArticleSchema


parser = reqparse.RequestParser()


class ArticleResource(Resource):
    method_decorators = {
        'post': [admin_required, token_required],
        'put': [admin_required, token_required],
        'delete': [admin_required, token_required]
    }

    def get(self, *args, **kwargs):
        parser.add_argument("ArticleID")
        args = parser.parse_args()
        article = Article.query.get(args['ArticleID'])
        if not article:
            return SysConfig.ReturnCode("ARTICLE_NOT_EXIST")
        article_schema = ArticleSchema()
        return article_schema.dump(article)

    def post(self, *args, **kwargs):
        try:
            parser.add_argument("Title")
            parser.add_argument("Text")
            parser.add_argument("UserID")
            args = parser.parse_args()
            new_artile = Article()
            new_artile.Title = args["Title"]
            new_artile.Text = args["Text"]
            new_artile.UserID = args["UserID"]
            new_artile.CreateDay = datetime.now()
            new_artile.CreateTime = datetime.now()
            new_artile.UpdateTime = datetime.now()
            db.session.add(new_artile)
            db.session.commit()
            return {"code": 200, "message": "添加成功!"}
        except Exception as e:
            return {"code": 204, "message": "添加失败!"+e}

    def put(self, *args, **kwargs):
        parser.add_argument("ArticleID")
        parser.add_argument("Title")
        parser.add_argument("Text")
        args = parser.parse_args()
        check_article = Article.query.get(args["ArticleID"])
        if not check_article:
            return SysConfig.ReturnCode("ARTICLE_NOT_EXIST")
        check_article.Title = args["Title"]
        check_article.Text = args["Text"]
        check_article.UpdateTime = datetime.now()
        try:
            db.session.commit()
            return SysConfig.ReturnCode("CHANGE_SUCCESS")
        except Exception as e:
            db.session.rollback()
            return {"code": 204, "message": f"添加失败!{str(e)}"}

    def delete(self, *args, **kwargs):
        parser.add_argument("ArticleID")
        args = parser.parse_args()
        check_article = Article.query.get(args["ArticleID"])
        if not check_article:
            return SysConfig.ReturnCode("ARTICLE_NOT_EXIST")
        db.session.delete(check_article)
        try:
            db.session.commit()
            return SysConfig.ReturnCode("DELETE_SUCCESS")
        except Exception as e:
            db.session.rollback()
            return {"code": 204, "message": f"删除失败!{str(e)}"}


class ArticleListResource(Resource):

    def get(self, *args, **kwargs):
        print("进入list")
        parser.add_argument("Page")
        args = parser.parse_args()
        page = int(args["Page"]) if args["Page"] else 1
        print("page", page, type(page))
        pagination = db.session.query(
            Article.ID, Article.Title
        ).paginate(page, per_page=8, error_out=False)
        articles = pagination.items
        article_schema = ArticleSchema(many=True)
        return article_schema.dump(articles)
