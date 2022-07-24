from flask import Flask

app = Flask(__name__)


app.config['SECRET_KEY'] = '22f32f52f73aeaf08ece955bdc6642e64f8004663bfeffa8'

from root import routes