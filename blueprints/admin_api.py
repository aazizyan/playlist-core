from flask import Blueprint, request, current_app

from model.db_functions import add_song, change_song_name, remove_song
from model.internal_config import DATABASE_CONNECTION
from objects.json_object import JsonObject

admin_api = Blueprint('admin', __name__,
                      url_prefix='/admin')


def get_connection():
    return current_app.config[DATABASE_CONNECTION]


@admin_api.route('/<place_id>/songs', methods=['POST'])
def new_song(place_id):
    """
    Adds song in given place's playlist
    :param place_id: unique place id
    :return: status
    """
    connection = get_connection()
    song = JsonObject(request.data.decode())
    if add_song(connection, place_id, song.username, song.songid):
        return '', 200
    return '', 404


@admin_api.route('/<place_id>/songs', methods=['PUT'])
def change_song(place_id):
    """
    Changes song's metadata
    :param place_id: unique place id
    :return: status
    """
    # TODO check validity
    connection = get_connection()
    song = JsonObject(request.data.decode())
    if change_song_name(connection, place_id, song.username,
                        song.songid, song.newname):
        return '', 200
    return '', 404


@admin_api.route('/<place_id>/songs', methods=['DELETE'])
def delete_song(place_id):
    """
    Deletes song from given place's list
    :param place_id: unique place id
    :return: status
    """
    # TODO check validity
    connection = get_connection()
    song = JsonObject(request.data.decode())
    if remove_song(connection, song.songid):
        return '', 200
    return '', 404
