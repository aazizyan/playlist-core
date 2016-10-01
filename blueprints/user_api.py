import json

from flask import Blueprint, request, current_app, make_response, redirect
from six import wraps

from model.db_functions import validate_user, add_user, \
    add_place, enter_place, like_song, get_songs, update_token, validate_token, get_song, get_places, is_admin, \
    place_location, get_admin
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
    user_info = validate_user(connection, username, password)
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
            resp = BuilderDict()
            resp.add("isadmin", is_admin(connection, user.username))
            resp.add("placeid", place_id)
            return resp.to_string(), 200
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


@user_api.route('/download/<songid>', methods=['GET'])
def donwload_song(songid):
    """
    User requests to download current playing song
    in given place.
    :param place_id: unique place id
    """
    # TODO handle request
    connection = get_connection()
    _bytes, name = get_song(connection, songid)
    response = make_response(bytes(_bytes))
    response.headers['Content-Type'] = 'audio/mpeg'
    response.headers['Content-Disposition'] = 'filename="{}"'.format(name)
    return response


def song_list_response(song_list):
    dict_list = list()
    for song in song_list:
        temp_dict = dict()
        temp_dict['songid'] = str(song[0])
        temp_dict['name'] = song[3]
        temp_dict['placeid'] = str(song[1])
        temp_dict['rating'] = song[4]
        dict_list.append(temp_dict)

    return dict_list


@user_api.route('/<place_id>/songs', methods=['POST'])
def get_list(place_id):
    """
    Returns list of songs for given place id
    :param place_id: urlparam place id
    :return:
    """
    connection = get_connection()
    # add_song(connection, "4", 'pppp', 'asd.mp3', open('/home/misho/PycharmProjects/playlist-core/asd.mp3', 'rb').read())
    song_list = get_songs(connection, int(place_id))
    if song_list:
        response = song_list_response(song_list)
        return json.dumps(response), 200
    return '', 404


def places_list_response(places_list):
    dict_list = list()
    for place in places_list:
        temp_dict = dict()
        temp_dict['placeid'] = str(place[0])
        temp_dict['name'] = place[2]
        temp_dict['lat'] = place[3]
        temp_dict['lon'] = place[4]
        dict_list.append(temp_dict)
    return dict_list


@user_api.route('/places', methods=['POST'])
@requires_auth
def get_place_list():
    """
    Returns list of places
    :return:
    """
    connection = get_connection()
    places_list = get_places(connection)

    if places_list:
        response = places_list_response(places_list)
        return json.dumps(response), 200
    return '', 404


@user_api.route('/share/<place_id>', methods=['GET'])
def share_location(place_id):
    connection = get_connection()
    try:
        location = place_location(connection, int(place_id))
        if location:
            url = 'http://maps.google.com/maps?daddr={0},{1}'.format(str(location[0]), str(location[1]))
            return redirect(url, code=302)
    except:
        pass
    return '', 44


@user_api.route('/like', methods=['POST'])
def like_song():
    _like = JsonObject(request.data)
    res = validate_token(current_app.config[DATABASE_CONNECTION],
                         _like.token, _like.username, LEASE_TIME)
    if res:
        like_song(current_app.config[DATABASE_CONNECTION], _like.username, _like.songid, _like.like)
        return '', 200
    return '', 400


@user_api.route('/songs', methods=['POST'])
def request_song():
    """
    request song
    :param data:
    :return:
    """
    req = JsonObject(request.data)
    res = validate_token(current_app.config[DATABASE_CONNECTION],
                         req.token, req.username, LEASE_TIME)
    if res:
        # TODO request for admin
        get_admin(current_app.config[DATABASE_CONNECTION], req.placeid)
        return ''
    return '', 400

# TODO add update method
