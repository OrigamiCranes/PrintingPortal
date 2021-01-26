from . import bp
from flask import render_template, make_response, request, session
from flask_login import login_required
#from flask_user roles_required

@bp.route('/')
@login_required
def index():
    return render_template('printing/index.html', title='Printing')
