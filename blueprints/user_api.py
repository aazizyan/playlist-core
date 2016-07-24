import json

from flask import Blueprint, request, current_app
from six import wraps

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
    return response.add('token', token)


def response_user(user_info):
    response = BuilderDict()
    response.add('nick', user_info[0])
    response.add('isadmin', user_info[1])
    response.add('placeid', str(user_info[2]))
    return response


def get_connection():
    return current_app.config[DATABASE_CONNECTION]


def check_auth(username, token):
    connection = get_connection()
    return validate_token(connection, token, username, LEASE_TIME)


def authenticate():
    return '', 401


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = JsonObject(request.data.decode())
        if not data or not check_auth(data.username, data.token):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


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
        response = response_token(token)
        if user.admin:
            place_id = add_place(connection, user.username,
                                 user.placename, user.lat, user.lon)
            if place_id is None:
                return '', 404
            response.add('id', str(place_id))
            return response.to_string(), 200
        return response.to_string(), 200
    return '', 404


@user_api.route('/login', methods=['POST'])
def login_user():
    """
    Checks requested username and password validity
    """
    connection = get_connection()
    user = JsonObject(request.data.decode())
    username = user.username
    password = hash_password(username, user.password)
    user_info = validate_user(connection, user.token, username, password)
    if user_info:
        token = update_token(connection, user.username)
        response = response_user(user_info).add('token', token).to_string()
        return response, 200
    return '', 404


@user_api.route('/check', methods=['POST'])
def check_validity():
    connection = get_connection()
    user = JsonObject(request.data.decode())
    response = None
    user_info = validate_token(connection, user.token, user.username, LEASE_TIME)
    if user_info:
        response = response_user(user_info).add("response", True)
    else:
        response = BuilderDict().add("response", False)
    return response.to_string(), 200


@user_api.route('/login/<place_id>', methods=['POSt'])
@requires_auth
def join_place(place_id):
    """
    Lets user join requested place.
    Server sends user all required information.
    :param place_id: unique place id
    """
    connection = get_connection()
    user = JsonObject(request.data.decode())
    try:
        if enter_place(connection, int(place_id)):
            return '', 200
    except:
        pass

    return '', 404


@user_api.route('/songs', methods=['PUT'])
@requires_auth
def send_like_song():
    """
    User likes or dislikes song in current place.
    :param place_id: unique place id
    """
    connection = get_connection()
    like = JsonObject(request.data.decode())
    if like_song(connection, like.username, like.songid, like.like):
        return '', 200
    return '', 404


@user_api.route('/<place_id>', methods=['POST'])
@requires_auth
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
@requires_auth
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


def song_list_response(song_list):
    dict_list = list()
    for song in song_list:
        temp_song_dict = BuilderDict()\
            .add('songid', str(song[0]))\
            .add('name', song[3])\
            .add('placeid', str(song[1]))\
            .add('raiting', song[4])
        dict_list.append(temp_song_dict)

    return dict_list


@user_api.route('/<place_id>/songs')
@requires_auth
def get_list(place_id):
    """
    Returns list of songs for given place id
    :param place_id: urlparam place id
    :return:
    """
    connection = get_connection()
    song_list = get_songs(connection, int(place_id))
    if song_list:
        response = song_list_response(song_list)
        return json.dumps(response), 200
    return '', 404


def places_list_response(places_list):
    dict_list = list()
    for place in places_list:
        temp_palce_dict = BuilderDict().\
            add('placeid', str(place[0])).\
            add('name', place[2]).\
            add('lat', place[3]).\
            add('lon', place[4])
        dict_list.append(temp_palce_dict)
    return dict_list


@user_api.route('/places')
@requires_auth
def get_places_list():
    """
    Returns list of places
    :return:
    """
    connection = get_connection()
    places_list = get_places_list(connection)
    if places_list:
        response = places_list_response(places_list)
        return json.dumps(response), 200
    return '', 404
