from flask import Flask, request
from flask_restful import Api, Resource
from user_comment_reaction import arr_append
from user_comment_reaction import reaction_functions
from discord_webhook import ngrok_public_url

app = Flask(__name__)
api = Api(app)


def checkPostedData(postedData, functionName):
    if functionName == "reaction":
        if "url" not in postedData or "reaction" not in postedData or "webhook_url" not in postedData:
            return 301
        else:
            return 200

    if functionName == "comment":
        if "url" not in postedData or "com" not in postedData or "webhook_url" not in postedData:
            return 301
        else:
            return 200


class Comment(Resource):
    def post(self):
        postedData = request.get_json()

        # CHECK DATA THROWN BY API IF COMPLETE
        status_code = checkPostedData(postedData, "comment")
        if status_code != 200:
            return {"Message": "Incomplete parameter",
                    "Status Code": status_code}
        # DATA FROM API
        url = postedData["url"]
        com = postedData["com"]
        webhook = postedData["webhook_url"]
        data = {'url': url, 'comment': com, 'reaction': "", 'webhook': webhook}
        arr_append(data)

        return {"Response": 200}


class Reaction(Resource):
    def post(self):
        postedData = request.get_json()

        # CHECK DATA THROWN BY API IF COMPLETE
        status_code = checkPostedData(postedData, "reaction")
        if status_code != 200:
            return {"Message": "Incomplete parameter",
                    "Status Code": status_code}
        # DATA FROM API
        url = postedData["url"]
        reaction = postedData["reaction"]
        webhook = postedData["webhook_url"]
        data = {'url': url, 'comment': "", 'reaction': reaction, 'webhook': webhook}
        reaction_functions(data)
        return {"Response": 200}


api.add_resource(Comment, "/comment")
api.add_resource(Reaction, "/reaction")

if __name__ == '__main__':
    # NGROK PUBLIC URL
    webhook_url = ""
    ngrok_public_url(webhook_url)
    app.debug = False
    app.run(use_reloader=False)


