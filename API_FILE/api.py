from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

ac = {1: "Marcin"}


class Example(Resource):
    def get(self):
        return {"Data": "numer "}


api.add_resource(Example, "/test")  # /video/<int:Account_id>

if __name__ == "__main__":
    app.run(debug=True)
