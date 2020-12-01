import datetime
import database


menu = """Выберете одну из предложенных опций:
1)Добавить новый фильм
2)Грядущие релизы
3)Посмотреть список всех фильмов
4)Отметить просмотренный фильм
5)Просмотреть список просмотренных фильмов
6)Добавить пользователя
7)Выход

Ваш выбор: """
welcome = "Добро пожаловать в органайзер фильмов!"

print(welcome)
database.create_tables()

def prompt_add_user():
    username = input("Введи имя: ")
    database.add_user(username)


def prompt_add_movie():
    title = input("Название фильма: ")
    release_date = input("Дата появления (дд.мм.гггг): ")
    print("---- \n")
    parsed_date = datetime.datetime.strptime(release_date, "%d.%m.%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    print(f"--{heading} фильмы--")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        normal_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} ({normal_date})")
    print("---- \n")


def prompt_watch_movie():
    username = input("Введи имя: ")
    movie_id = input("Введите ID фильма: ")
    database.watch_movie(username, movie_id)
    print("---- \n")


def prompt_show_watched_movies():
    username = input("Введи имя: ")
    movies = database.get_watched_movies(username)
    if movies:
        print_movie_list(f"{username}", movies)
    else:
        print("Список пуст!")


while (user_input := input(menu)) != "7":
    if user_input == '1':
        prompt_add_movie()
    elif user_input == '2':
        movies = database.get_movies(True)
        print("Бяка")
        print_movie_list("Грядущие", movies)
    elif user_input == '3':
        movies = database.get_movies()
        print_movie_list("Все", movies)
    elif user_input == '4':
        prompt_watch_movie()
    elif user_input == '5':
        prompt_show_watched_movies()
    elif user_input == '6':
        prompt_add_user()
    else:
        print("Неверная команда, попробуйте еще раз")
