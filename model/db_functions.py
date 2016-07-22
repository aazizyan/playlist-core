import uuid

def add_user(connection, username, password, name, is_admin):
    cursor = connection.cursor()
    try:
        token = uuid.uuid1().hex
        cursor.execute("""INSERT INTO users (username, password, name, is_admin, token) VALUES (%s, %s, %s, %s, %s);""",
                       (username, password, name, is_admin, token))
    except:
        return None
    connection.commit()
    return token


def validate_user(connection, username, password):
    cursor = connection.cursor()

    cursor.execute("""SELECT password FROM users WHERE username = %s;""",
                   (username,))
    if cursor.rowcount == 0:
        return False
    row = cursor.fetchone()
    return row[0] == password


def add_place(connection, admin_id, place_name, latitude, longtitude):
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO places (user_id, place_name, latitude, longitude) VALUES (%s, %s, %s, %s);""",
                   (admin_id, place_name, latitude, longtitude))
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def add_song(connection, place_id, username, song_name):
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO songs (place_id, username, song_name) VALUES (%s, %s, %s);""",
                   (place_id, username, song_name))
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def like_song(connection, user_id, song_id, _type):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM likes WHERE  user_id = %s and song_id = %s""",
                   (user_id, song_id))

    if cursor.rowcount > 0:
        like = cursor.fetchone()
        if like[3] == _type:
            return False
        else:
            cursor.execute("""UPDATE likes SET type = %s WHERE user_id = %s and song_id = %s""",
                           (_type, user_id, song_id))
            connection.commit()
            return True

    cursor.execute("""INSERT INTO likes (user_id, song_id, type) VALUES (%s, %s, %s);""",
                   (user_id, song_id, _type))
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def remove_song(connection, song_id):
    cursor = connection.cursor()

    cursor.execute("""DELETE From likes WHERE song_id = %s;""",
                   (song_id,))

    cursor.execute("""DELETE FROM songs WHERE song_id = %s;""",
                   (song_id,))

    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def validate_token(connection, user_id, lapse_time):
    cursor = connection.cursor()
    cursor.execute(
        """SELECT token_date FROM users WHERE user_id = %s and EXTRACT(EPOCH FROM now()) - %s <= token_date""",
        (user_id, lapse_time))
    if cursor.rowcount == 1:
        cursor.execute("""UPDATE users SET token_date = EXTRACT(EPOCH FROM now()) WHERE user_id = %s""",
                       (user_id,))
        connection.commit()
        return True
    return False


def update_token(connection, user_id):
    cursor = connection.cursor()
    token = uuid.uuid1().hex
    try:
        cursor.execute("""UPDATE users SET token = %s WHERE user_id = %s""",
                       (token, user_id))
    except:
        return None
    connection.commit()
    return token


def enter_place(connection, username, placeid):
    pass


def change_song_name(connection, song_id, new_name):
    cursor = connection.cursor()
    cursor.execute("""UPDATE songs SET song_name = %s WHERE song_id = %s""",
        (new_name, song_id))
    connection.commit()


def get_songs(connection, place_id):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM songs WHERE place_id = %s""",
        (place_id,))
    songs_list = cursor.fetchall()
    return songs_list
