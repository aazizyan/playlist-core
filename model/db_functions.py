import uuid

import psycopg2


def add_user(connection, username, password, name, is_admin):
    cursor = connection.cursor()
    try:
        token = uuid.uuid1().hex
        cursor.execute("""INSERT
                            INTO users (username, password, name, is_admin, token)
                            VALUES (%s, %s, %s, %s, %s);""",
                       (username, password, name, is_admin, token))
    except psycopg2.IntegrityError:
        return None
    connection.commit()
    return token


def validate_user(connection, username, password):
    cursor = connection.cursor()

    cursor.execute("""SELECT password
                        FROM users
                        WHERE username = %s;""",
                   (username,))
    if cursor.rowcount == 0:
        return False
    row = cursor.fetchone()
    return row[0] == password


def add_place(connection, admin_username, place_name, latitude, longtitude):
    cursor = connection.cursor()

    cursor.execute("""INSERT
                        INTO places (username, place_name, latitude, longitude)
                        VALUES (%s, %s, %s, %s);""",
                   (admin_username, place_name, latitude, longtitude))
    if cursor.rowcount == 0:
        return None
    cursor.execute("""SELECT currval('places_place_id_seq')""")
    place_id = cursor.fetchone()[0]
    connection.commit()
    return place_id


def add_song(connection, place_id, username, song_name):
    cursor = connection.cursor()

    cursor.execute("""INSERT
                        INTO songs (place_id, username, song_name)
                        VALUES (%s, %s, %s);""",
                   (place_id, username, song_name))
    if cursor.rowcount == 0:
        return None
    cursor.execute("""SELECT currval('songs_song_id_seq')""")
    song_id = cursor.fetchone()[0]
    connection.commit()
    return song_id


def like_song(connection, username, song_id, _type):
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                        FROM likes
                        WHERE   username = %s and
                                song_id = %s""",
                   (username, song_id))

    if cursor.rowcount > 0:
        like = cursor.fetchone()
        if like[3] == _type:
            return False
        else:
            cursor.execute("""UPDATE likes
                                SET type = %s
                                WHERE username = %s and
                                      song_id = %s""",
                           (_type, username, song_id))
            connection.commit()
            return True

    cursor.execute("""INSERT
                        INTO likes (username, song_id, type)
                        VALUES (%s, %s, %s);""",
                   (username, song_id, _type))
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def remove_song(connection, song_id):
    cursor = connection.cursor()
    cursor.execute("""DELETE
                        From likes
                        WHERE song_id = %s;""",
                   (song_id,))

    cursor.execute("""DELETE
                        FROM songs
                        WHERE song_id = %s;""",
                   (song_id,))

    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def validate_token(connection, username, lapse_time):
    cursor = connection.cursor()
    cursor.execute("""SELECT token_date
                        FROM users
                        WHERE username = %s and
                              EXTRACT(EPOCH FROM now()) - %s <= token_date""",
                    (username, lapse_time))
    if cursor.rowcount == 1:
        cursor.execute("""UPDATE users
                            SET token_date = EXTRACT(EPOCH FROM now())
                            WHERE username = %s""",
                       (username,))
        connection.commit()
        return True
    return False


def update_token(connection, username):
    cursor = connection.cursor()
    token = uuid.uuid1().hex
    cursor.execute("""UPDATE users
                        SET token = %s
                        WHERE username = %s""",
                   (token, username))
    connection.commit()
    return token


def enter_place(connection, username, placeid):
    pass


def change_song_name(connection, song_id, new_name):
    cursor = connection.cursor()
    cursor.execute("""UPDATE songs
                        SET song_name = %s
                        WHERE song_id = %s""",
                   (new_name, song_id))
    connection.commit()


def get_songs(connection, place_id):
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                        FROM songs
                        WHERE place_id = %s""",
                    (place_id,))
    if cursor.rowcount == 0:
        return []
    songs_list = cursor.fetchall()
    return songs_list

