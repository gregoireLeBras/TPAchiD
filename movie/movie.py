from ariadne import graphql_sync, load_schema_from_path, ObjectType, QueryType, make_executable_schema, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys

import resolver as r
from graphql.type import schema
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

type_defs = load_schema_from_path('movie.graphql')

movie = ObjectType('Movie')

query = QueryType()
query.set_field('all_movies', r.all_movies)
query.set_field('get_movie_by_id', r.get_movie_by_id)
query.set_field('get_movie_by_title', r.get_movie_by_title)

mutation = MutationType()
mutation.set_field('create_movie', r.create_movie)
mutation.set_field('delete_movie', r.delete_movie)
mutation.set_field('update_movie_title', r.update_movie_title)

schema = make_executable_schema(type_defs, movie, query, mutation)
'''with open('{}/databases/movies.json'.format("."), "r") as jsf:
   movies = json.load(jsf)["movies"]'''

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
