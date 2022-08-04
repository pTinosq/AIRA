from flask import jsonify, render_template, request
import base64
import ast
import uncertainpy.argumentation as arg
from uncertainpy.argumentation import Argument
from uncertainpy.argumentation.graphing import graph
from .formDataHandler import graph_from_ls, isBase64

from root import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/api/draw_graph', methods=['GET'])
def api_draw_graph():
    d = request.args.get('d')
    print(d)
    if (isBase64(d)):
        q = ast.literal_eval(base64.b64decode(d).decode())
        t = graph_from_ls(q)
        return jsonify(t)
    else:
        return jsonify([False, 'Invalid data'])


@app.route('/line_graph')
def line_graph():
    return render_template('line_graph.html', title='Line graph')
