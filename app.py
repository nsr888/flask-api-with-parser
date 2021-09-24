from flask import Flask
from flask_restful import Api
from resources.ok.friends import OkFriends


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(OkFriends, "/ok/friends", endpoint="ok")
    app.config["RESTFUL_JSON"] = {"ensure_ascii": False}
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
