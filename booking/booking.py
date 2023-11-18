from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
   """
   renvois tout les bookings

   :return: json de tout les bookings
   """
   res = make_response(jsonify(bookings), 200)
   return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
   """
   récupère la liste des bookings d'un utilisateur

   :param userid: id de l'utilisateur
   :return: json des bookings de l'utilisateur ou erreur
   """
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         return make_response(jsonify(booking), 200)
   return make_response(jsonify({"error": "bad input parameter"}), 400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   """
   ajoute un booking pour un user

   corps req : booking sous forme json

   :param userid: id utilisateur
   :return: le booking ajouté
   """
   req = request.get_json()
   r = requests.get('http://192.168.1.12:3202/showmovies/' + req["date"])
   if r.status_code == 200:
      if req["movieid"] in r.json()["movies"]:
         one_booking = {
            "date": req["date"],"movies": [req["movieid"]]
         }

         for item in bookings:
            if item["userid"] == userid:
               if one_booking not in item["dates"]:
                  item["dates"].append(one_booking)
                  return make_response(jsonify(one_booking),200)
               return make_response(jsonify({"error":"an existing item already exists"}),409)
   return make_response(jsonify({"error":"cannot add booking"}),400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
