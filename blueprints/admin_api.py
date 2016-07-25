from flask import Blueprint, request, current_app
from six import wraps

from model.db_functions import add_song, change_song_name, remove_song, validate_token
from model.internal_config import DATABASE_CONNECTION
from model.utils import LEASE_TIME
from objects.builder_dict import BuilderDict
from objects.json_object import JsonObject
from blueprints.user_api import check_auth, authenticate, requires_auth
from model.db_functions import validate_admin
admin_api = Blueprint('admin', __name__,
                      url_prefix='/admin')


def get_connection():
    return current_app.config[DATABASE_CONNECTION]


def check_admin_auth(place_id, admin_username):
    connection = get_connection()
    return validate_admin(connection, place_id, admin_username)


def admin_authenticate():
    return '', 401


def requires_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = JsonObject(request.data.decode())
        if not data or not check_admin_auth(data.place_id, data.username):
            return admin_authenticate()
        return f(*args, **kwargs)
    return decorated


@admin_api.route('/<place_id>/songs', methods=['POST'])
# @requires_auth
# @requires_admin_auth
def new_song(place_id):
    """
    Adds song in given place's playlist
    :param place_id: unique place id
    :return: status
    """
    connection = get_connection()
    song = JsonObject(request.data.decode())
    if not validate_token(connection, song.token, song.username, LEASE_TIME):
        return BuilderDict.create_update_lease()
    if 'file' in request.files:
        _file = request.files['file']
        song_id = add_song(connection, place_id, song.token, song.username, _file.read())
        if song_id:
            response = BuilderDict()
            return response.add('id', str(song_id)).to_string(), 200
    return '', 404


@admin_api.route('/<place_id>/songs', methods=['PUT'])
# @requires_auth
# @requires_admin_auth
def change_song(place_id):
    """
    Changes song's metadata
    :param place_id: unique place id
    :return: status
    """

    connection = get_connection()
    song = JsonObject(request.data.decode())
    if not validate_token(connection, song.username, LEASE_TIME):
        return BuilderDict.create_update_lease()
    if change_song_name(connection, place_id, song.username):
        return '', 200
    return '', 404


@admin_api.route('/<place_id>/songs', methods=['DELETE'])
# @requires_auth
# @requires_admin_auth
def delete_song(place_id):
    """
    Deletes song from given place's list
    :param place_id: unique place id
    :return: status
    """
    # TODO check validity
    connection = get_connection()
    song = JsonObject(request.data.decode())
    if not validate_token(connection, song.username, LEASE_TIME):
        return BuilderDict.create_update_lease()
    if remove_song(connection, song.songid):
        return '', 200
    return '', 404
