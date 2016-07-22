import json

from flask import Blueprint, request, current_app

from model.db_functions import validate_user, add_user, \
    add_place, enter_place, like_song, get_songs, update_token, validate_token
from model.internal_config import DATABASE_CONNECTION
from model.utils import hash_password, LEASE_TIME
from objects.builder_dict import BuilderDict
from objects.json_object import JsonObject

user_api = Blueprint('user', __name__,
                     url_prefix='/user')


def response_token(token):
    response = BuilderDict()
    return response.add('token', token).to_string()


def get_connection():
    return current_app.config[DATABASE_CONNECTION]


@user_api.route('/', methods=['POST'])
def create_user():
    """
    Adds new user
    """
    connection = get_connection()
    user = JsonObject(request.data.decode())
    username = user.username
    password = hash_password(username, user.password)
    token = add_user(connection, username, password,
                     user.name, user.admin)
    if token:
        if user.admin:
            if not add_place(connection, user.username,
                             user.place, user.lat, user.lon):
                return '', 404
        return response_token(token), 200
    return '', 404


@user_api.route('/login', methods=['POST'])
def get_user():
    """
    Checks requested username and password validity
    """
    connection = get_connection()
    user = JsonObject(request.data.decode())
    username = user.username
    password = hash_password(username, user.password)
    if validate_user(connection, username, password):
        token = update_token(connection, user.username)
        return response_token(token), 200
    return '', 404


@user_api.route('/login/<place_id>')
def join_place(place_id):
    """
    Lets user join requested place.
    Server sends user all required information.
    :param place_id: unique place id
    """
    connection = get_connection()
    user = JsonObject(request.data.decode())
    if not validate_token(connection, user.username, LEASE_TIME):
        return BuilderDict.create_update_lease()
    if enter_place(connection, user.username, place_id):
        return '', 200
    return '', 404


@user_api.route('/songs>', methods=['PUT'])
def send_like_song():
    """
    User likes or dislikes song in current place.
    :param place_id: unique place id
    """
    connection = get_connection()
    like = JsonObject(request.data.decode())
    if not validate_token(connection, like.username, LEASE_TIME):
        return BuilderDict.create_update_lease()
    if like_song(connection, like.username, like.songid, like.like):
        return '', 200
    return '', 404


@user_api.route('/<place_id>', methods=['POST'])
def request_song(place_id):
    """
    User sends request to add
    new song in current playlist
    :param place_id: unique place id
    """
    # TODO handle request
    connection = get_connection()
    song = JsonObject(request.data.decode())

    return 'request song'


@user_api.route('/download/<place_id>/song', methods=['GET'])
def donwload_song(place_id):
    """
    User requests to download current playing song
    in given place.
    :param place_id: unique place id
    """
    # TODO handle request
    connection = get_connection()
    song = JsonObject(request.data.decode())
    return 'song song'


@user_api.route('/<place_id>/songs')
def get_list(place_id):
    """
    Returns list of songs for given place id
    :param place_id: urlparam place id
    :return:
    """
    connection = get_connection()
    response = get_songs(connection, place_id)
    if response:
        return json.dumps(response), 200
    return '', 404
