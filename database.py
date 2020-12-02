import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    Название TEXT, 
    Дата_релиза REAL
); """

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    Имя_пользователя TEXT PRIMARY KEY
); """

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    Имя_аккаунта TEXT, 
    id_фильма INTEGER,
    FOREIGN KEY (Имя_аккаунта) REFERENCES users(Имя_пользователя), 
    FOREIGN KEY (id_фильма) REFERENCES movies(id)
); """

INSERT_MOVIES = "INSERT INTO movies (Название, Дата_релиза) VALUES (?, ?);"
INSERT_USERS = "INSERT INTO users (Имя_пользователя) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE Название = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE Дата_релиза > ?;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies 
JOIN watched ON movies.id = watched.id_фильма
JOIN users ON users.Имя_пользователя = watched.Имя_аккаунта
WHERE users.Имя_пользователя = ?;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (Имя_аккаунта, id_фильма) VALUES (?, ?); "
SET_MOVIE_WATCHED = "UPDATE movies SET Просмотрено = 1 WHERE Название = ?;"
SEARCH_MOVIE = "SELECT * FROM movies WHERE Название LIKE ?;"
#CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_релиз_фильма ON movies(Дата_релиза);"

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        #connection.execute(CREATE_RELEASE_INDEX)



def add_user(username):
    with connection:
        connection.execute(INSERT_USERS, (username,))


def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def search_movie(search_term):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
        return cursor.fetchall()

def watch_movie(username, movie_id):
    with connection:
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))
        return cursor.fetchall()


def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()
