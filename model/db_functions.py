def add_user(connection, username, password, name, is_admin, token):
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO users (username, password, name, is_admin, token) VALUES (%s, %s, %s, %s, %s);""",
                       (username, password, name, is_admin, token))
    except:
        return False
    connection.commit()
    return True


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


def add_song(connection, place_id, user_id, song_name):
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO songs (place_id, user_id, song_name) VALUES (%s, %s, %s);""",
                   (place_id, user_id, song_name))
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def like_song(connection, user_id, song_id, type):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM likes WHERE  user_id = %s and song_id = %s""",
                   (user_id, song_id))

    if cursor.rowcount > 0:
        like = cursor.fetchone()
        if like[3] == type:
            return False
        else:
            cursor.execute("""UPDATE likes SET type = %s WHERE user_id = %s and song_id = %s""",
                           (type, user_id, song_id))
            connection.commit()
            return True

    cursor.execute("""INSERT INTO likes (user_id, song_id, type) VALUES (%s, %s, %s);""",
                   (user_id, song_id, type))
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


def enter_place(connection, username, placeid):
    pass


def change_song_name(connection, place_id, user_id, song_name, new_name):
    pass


def get_songs(connection, place_id):
    pass
