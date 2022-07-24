from flask import Flask
import json

app = Flask(__name__)
with open("__private__/config.json", "r") as f:
    data = json.load(f)
    app.config['SECRET_KEY'] = data["SECRET_KEY"]
    

from root import routes