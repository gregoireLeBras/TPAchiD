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
   return make_response(jsonify(users), 200)

@app.route("/user/bookings/<useridorname>", methods=['GET'])
def get_booking_for_user(useridorname):
   if " " in useridorname:
      userid = useridorname.replace(" ", "_").lower()
   req = requests.get('http://192.168.1.12:3201/bookings/' + userid)
   if req.status_code == 200:
      return make_response(req.json(), 200)
   return make_response(jsonify({"error":"Invalid user id"}), 400)


@app.route("/user/getMoviesInfo/<userid>", methods=['GET'])
def getMoviesInfo(userid):
   bookings = requests.get('http://192.168.1.12:3201/bookings/' + userid)
   movieDetailsArr = []
   if bookings.status_code == 200:
      print(bookings.json())
      for date in bookings.json()['dates']:
         for movieId in date['movies']:
            movieDetails = requests.get('http://192.168.1.12:3200/movies/' + movieId)
            movieDetailsArr.append(movieDetails.json())
      return make_response(jsonify(movieDetailsArr), 200)
   return make_response(jsonify({"error":"Invalid user id"}), 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
