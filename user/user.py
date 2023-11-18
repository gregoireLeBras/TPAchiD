from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_json():
   """
      permet de recuperer les utilisateurs

      :return: json de tous les utilisateurs
      """
   return make_response(jsonify(users), 200)

@app.route("/user/bookings/<useridorname>", methods=['GET'])
def get_booking_for_user(useridorname):
   """
      requette booking

      :param stub: stub de booking
      :param userid: id de l'utilisateur
      :return: les bookings lié à l'utilisateur
      """
   if " " in useridorname:
      userid = useridorname.replace(" ", "_").lower()
   req = requests.get('http://192.168.1.12:3201/bookings/' + userid)
   if req.status_code == 200:
      return make_response(req.json(), 200)
   return make_response(jsonify({"error":"Invalid user id"}), 400)


@app.route("/user/getMoviesInfo/<userid>", methods=['GET'])
def getMoviesInfo(userid):
   """
      recupère les bookings d'un utilisateur

      :param userid: id de l'utilisateur
      :return: dictionnaire des bookings lié à l'utilisateur
      """
   bookings = requests.get('http://192.168.1.12:3201/bookings/' + userid)
   movieDetailsArr = []
   if bookings.status_code == 200:
      for date in bookings.json()['dates']:
         for movieId in date['movies']:
            query = '''
            query Get_movie_by_id {
               get_movie_by_id(_id: "''' + movieId +'''") {
                  id
                  title
                  director
                  rating
               }
            }
            '''
            movieDetails = requests.post('http://192.168.1.12:3200/graphql', json={'query': query})
            movieDetailsArr.append(movieDetails.json()["data"]["get_movie_by_id"])
      return make_response(jsonify(movieDetailsArr), 200)
   return make_response(jsonify({"error":"Invalid user id"}), 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
