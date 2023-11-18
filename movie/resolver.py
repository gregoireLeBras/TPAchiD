import json

def all_movies(_, info):
    """
    retourne tout les movies

    :param _:
    :param info:
    :return: liste de movies
    """
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies["movies"]

def get_movie_by_id(_, info, _id):
    """
    retourne un movie selon son id

    :param _:
    :param info:
    :param _id: id du movie
    :return: retourne infos du movie
    """
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["id"] == str(_id):
                return movie

def get_movie_by_title(_, info, _title):
    """
    retourne informations d'un movie selon son nom

    :param _:
    :param info:
    :param _title: nom du movie
    :return: informations du movie
    """
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["title"] == str(_title):
                return movie

def create_movie(_, info,_id, _title, _director, _rating):
    """
    créer un movie
    :param _:
    :param info:
    :param _id: id du movie
    :param _title: titre du movie
    :param _director: director du movie
    :param _rating: note du movie
    :return:
    """
    movies = []
    movie = {'title' : _title, "rating" : _rating, "director" : _director, "id" : _id}
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        movies.append(movie)
    with open('{}/databases/movies.json'.format("."), "w") as file:
        json.dump({"movies": movies}, file)
    return movie

def delete_movie(_, info, _id):
    """
    supprime un movie
    :param _:
    :param info:
    :param _id: id du movie à supprimer
    :return: movie supprimé
    """
    movie_to_delete = None;
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["id"] == _id:
                movie_to_delete = movie
                movies.remove(movie)
    with open('{}/databases/movies.json'.format("."), "w") as file:
        json.dump({"movies": movies}, file)
    return movie_to_delete

def update_movie_title(_, info, _id, _title):
    """
    met à jour la date d'un film
    :param _:
    :param info:
    :param _id: id du movie
    :param _title: nouveau titre
    :return: movie modifié
    """
    renamed_movie = None;
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["id"] == _id:
                movie["title"] = _title
                renamed_movie = movie
    with open('{}/databases/movies.json'.format("."), "w") as file:
        json.dump({"movies": movies}, file)
    return renamed_movie

