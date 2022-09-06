from flask import jsonify, render_template, request
import base64
import ast
from .formDataHandler import graph_from_ls, vbo_from_ls, nodes_from_ls, isBase64

from . import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/api/draw_graph', methods=['GET'])
def api_draw_graph():
    d = request.args.get('d')
    if (isBase64(d)):
        q = ast.literal_eval(base64.b64decode(d).decode())
        t = graph_from_ls(q)
        return jsonify(t)
    else:
        return jsonify([False, 'Invalid Data', 'Something has gone very wrong. Please refresh the webpage.'])


@app.route('/api/draw_nodes', methods=['GET'])
def api_draw_nodes():
    d = request.args.get('d')
    if (isBase64(d)):
        q = ast.literal_eval(base64.b64decode(d).decode())
        t = nodes_from_ls(q)
        return jsonify(t)
    else:
        return jsonify([False, 'Invalid Data', 'Something has gone very wrong. Please refresh the webpage.'])


@app.route('/api/fetch_verbose_output', methods=['GET'])
def api_fetch_verbose_output():
    d = request.args.get('d')
    if (isBase64(d)):
        q = ast.literal_eval(base64.b64decode(d).decode())
        t = vbo_from_ls(q)
        return jsonify(t)
    else:
        return jsonify([False, 'Invalid Data', 'Something has gone very wrong. Please refresh the webpage.'])


@app.route('/line_graph')
def line_graph():
    return render_template('line_graph.html', title='Line graph')

@app.route('/node_graph')
def node_graph():
    return render_template('node_graph.html', title='Node graph')

@app.route('/verbose_output')
def verbose_output():
    return render_template('verbose_output.html', title='Verbose output')
