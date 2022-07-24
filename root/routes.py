from flask import  render_template
import uncertainpy.argumentation as arg
from uncertainpy.argumentation import Argument
from uncertainpy.argumentation.graphing import graph
from root import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    return render_template('home.html', title='Home')
    