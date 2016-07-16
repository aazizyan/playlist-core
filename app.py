import os

from flask import Flask

from blueprints import test

app = Flask(__name__)
app.register_blueprint(test)


@app.route('/ping')
def ping():
    return '', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
