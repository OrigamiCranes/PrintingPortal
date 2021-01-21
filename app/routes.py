from app import app
from flask import render_template, make_response, request, session


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')