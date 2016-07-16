import os

from flask import Flask

from blueprints import ping

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(ping)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
