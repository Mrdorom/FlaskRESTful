from flask_restful import Resource, reqparse

from app import db
from .models import New
from .schema import NewSchema


parser = reqparse.RequestParser()


class NewResource(Resource):

    def get(self, *args, **kwargs):
        print("开始获取新闻")
        parser.add_argument("Page")
        args = parser.parse_args()
        print("====", args)
        page = int(args["Page"]) if args["Page"] else 1
        print("page", page, type(page))
        pagination = db.session.query(
            New.ID, New.Title, New.Url
        ).order_by(db.desc(New.ID)).paginate(page, per_page=8, error_out=False)
        news = pagination.items
        news_schema = NewSchema(many=True)
        return news_schema.dump(news)
