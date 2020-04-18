from flask_restful import Resource, reqparse
from GBComments import produceComments

parser = reqparse.RequestParser()


class GBComment(Resource):

    def get(self, *args, **kwargs):
        parser.add_argument("Type")
        parser.add_argument("Class")
        args = parser.parse_args()
        if args["Class"]:
            comments = produceComments(args["Type"], args["Class"])
        else:
            comments = produceComments(_type=args["Type"])
        return {"code": 200, "message": comments}
