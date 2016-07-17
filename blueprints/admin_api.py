from flask import Blueprint

admin_api = Blueprint('admin', __name__,
                      url_prefix='/admin')


@admin_api.route('/<place_id>/songs', methods=['POST'])
def add_song(place_id):
    """
    Adds song in given place's playlist
    :param place_id: unique place id
    :return: status
    """
    return 'song added'


@admin_api.route('/<place_id>/songs', methods=['PUT'])
def change_song(place_id):
    """
    Changes song's metadata
    :param place_id: unique place id
    :return: status
    """
    return 'changed'


@admin_api.route('/<place_id>/songs', methods=['DELETE'])
def remove_song(place_id):
    """
    Deletes song from given place's list
    :param place_id: unique place id
    :return: status
    """
    return 'removed'
