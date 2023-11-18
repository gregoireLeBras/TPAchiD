import json

def all_movies(_, info):
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies["movies"]

def get_movie_by_id(_, info, _id):
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["id"] == str(_id):
                return movie

def get_movie_by_title(_, info, _title):
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["title"] == str(_title):
                return movie

def create_movie(_, info,_id, _title, _director, _rating):
    movies = []
    movie = {'title' : _title, "rating" : _rating, "director" : _director, "id" : _id}
    with open('{}/databases/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        movies.append(movie)
    with open('{}/databases/movies.json'.format("."), "w") as file:
        json.dump({"movies": movies}, file)
    return movie

def delete_movie(_, info, _id):
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

