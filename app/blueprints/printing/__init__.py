from flask import Blueprint, url_for


bp = Blueprint('printing', __name__,template_folder='templates')

from . import routes, forms

