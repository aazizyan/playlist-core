import os
from urllib.parse import uses_netloc, urlparse

import psycopg2
from flask import Flask

from blueprints import user_api, admin_api
from model.internal_config import DATABASE_CONNECTION, DATABASE_URL

app = Flask(__name__)

app.register_blueprint(user_api)
app.register_blueprint(admin_api)

uses_netloc.append("postgres")
url = urlparse(DATABASE_URL)

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

app.config[DATABASE_CONNECTION] = conn


@app.errorhandler(AttributeError)
def err_handler(err):
    return err.message, 400


@app.route('/ping')
def ping():
    return '', 200


# @app.route('/db_test')
# def db_test():
#     connection = app.config[DATABASE_CONNECTION]
#     return str(connection.closed), (200 if connection.closed == 0 else 404)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
