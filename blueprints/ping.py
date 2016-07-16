"""
Ping blueprint
"""

from flask import Blueprint

ping = Blueprint('pint', __name__, url_prefix='/ping')


@ping.route('/')
def ping_response():
    return '', 200
