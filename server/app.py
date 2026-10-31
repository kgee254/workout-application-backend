from flask import Flask, jsonify
from flask_migrate import Migrate

from server.models import db
from server.routes import api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api)

@app.route("/")
def home():
    return jsonify({"message": "Workout API is running"})


if __name__ == "__main__":
    app.run(port=5555, debug=True)