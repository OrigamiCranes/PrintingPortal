from . import bp
from flask import render_template, make_response, request, session


@bp.route('/')
def index():
    return render_template('printing/index.html', title='Printing')
