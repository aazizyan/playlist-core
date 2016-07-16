from flask import Flask

from blueprints import ping

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(ping)
    app.run(debug=True)
