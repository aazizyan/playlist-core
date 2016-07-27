import os
from urllib.parse import uses_netloc, urlparse

import psycopg2
from flask import Flask
from flask_socketio import SocketIO, emit, leave_room, join_room

from blueprints import user_api, admin_api
from model.db_functions import validate_token, get_admin, is_admin, like_song
from model.internal_config import DATABASE_CONNECTION, DATABASE_URL
from model.utils import LEASE_TIME
from objects.builder_dict import BuilderDict
from objects.json_object import JsonObject

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

socketio = SocketIO(app)


@socketio.on('enter room')
def handle_message(data):
    user = JsonObject(data)
    join_room(user.placeid)
    if is_admin(app.config[DATABASE_CONNECTION], user.username):
        join_room(user.username)


@socketio.on('update msg')
def update_list(data):
    user = JsonObject(data)
    tempDict = BuilderDict().add('songid', user.songid)
    emit("change song", tempDict.to_string(), room=user.placeid)


@socketio.on('like')
def like(data):
    _like = JsonObject(data)
    res = validate_token(app.config[DATABASE_CONNECTION],
                         _like.token, _like.username, LEASE_TIME)
    if res:
        res = like_song(app.config[DATABASE_CONNECTION], _like.username, _like.songid, _like.like)
    if res:
        obj = BuilderDict()
        obj.add('songid', _like.songid)
        obj.add('like', _like.like)
        emit('like', obj.to_string(), room=_like.placeid)


@socketio.on('change song')
def change_song(data):
    song = JsonObject(data)
    emit('change song', 'changed', room=song.placeid)


@socketio.on('request song')
def request_song(data):
    req = JsonObject(data)
    res = validate_token(app.config[DATABASE_CONNECTION],
                         req.token, req.username, LEASE_TIME)
    if res:
        admin = get_admin(app.config[DATABASE_CONNECTION], req.placeid)
        obj = BuilderDict()
        obj.add('name', req.songname)
        emit('request song', obj.to_string(), room=admin)


@socketio.on('leave room')
def leave(data):
    user = JsonObject(data)
    leave_room(user.placeid)
    if is_admin(app.config[DATABASE_CONNECTION], user.username):
        leave_room(user.username)


@app.errorhandler(AttributeError)
def err_handler(err):
    return err.message, 400


@app.route('/ping')
def ping():
    return '', 200


@app.route('/db_test')
def db_test():
    connection = app.config[DATABASE_CONNECTION]
    return str(connection.closed), (200 if connection.closed == 0 else 404)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='192.168.43.219')
