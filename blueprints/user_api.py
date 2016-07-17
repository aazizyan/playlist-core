from flask import Blueprint, request

user_api = Blueprint('user', __name__,
                     url_prefix='/user')


@user_api.route('/', methods=['POST'])
def add_user():
    """
    Adds new user
    """
    return 'user added'


@user_api.route('/login', methods=['POST'])
def get_user():
    """
    Checks requested username and password validity
    """
    return 'faqfaq user'


@user_api.route('/login/<place_id>')
def join_place(place_id):
    """
    Lets user join requested place.
    Server sends user all required information.
    :param place_id: unique place id
    """
    return 'joined'


@user_api.route('/<place_id>', methods=['PUT'])
def like_song(place_id):
    """
    User likes or dislikes song in current place.
    :param place_id: unique place id
    """
    return 'likelike'


@user_api.route('/<place_id>', methods=['POST'])
def request_song(place_id):
    """
    User sends request to add
    new song in current playlist
    :param place_id: unique place id
    """
    return 'request song'


@user_api.route('/download/<place_id>/song', methods=['GET'])
def donwload_song(place_id):
    """
    User requests to download current playing song
    in given place.
    :param place_id: unique place id
    """
    return 'song song'
