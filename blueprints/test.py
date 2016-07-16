from flask import Blueprint

test = Blueprint('test', __name__)


@test.route('/test')
def return_val():
    return 'faqiu test'
