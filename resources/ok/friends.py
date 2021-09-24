import time
from flask_restful import Resource, reqparse
from flask import abort
from common.get_html import get_ok_friends_html
from common.parse_html import parse_friends_html


class OkFriends(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int)
        parser.add_argument("limit", type=int)
        parser.add_argument("timeout", type=int)
        args = parser.parse_args()

        if args["id"] is None or args["limit"] is None or args["timeout"] is None:
            abort(400)

        args["start_time"] = time.time()
        args["login"] = "79112587299"
        args["password"] = "19734682"

        html = get_ok_friends_html(args)
        friends_arr = parse_friends_html(html, args["limit"])
        return {"result": friends_arr}
