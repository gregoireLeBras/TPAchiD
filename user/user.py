from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import grpc
from google.protobuf.json_format import MessageToDict
from grpc._channel import _MultiThreadedRendezvous
from werkzeug.exceptions import NotFound
import bookings_pb2
import bookings_pb2_grpc
import times_pb2_grpc
import times_pb2

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

def get_bookings(stub, userid):
   bookings = stub.GetBookingByUser(bookings_pb2.User(user=userid))
   return bookings

@app.route("/user/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
   with grpc.insecure_channel('localhost:3201') as channel:
      return_dict = []
      if " " in userid:
         userid = userid.replace(" ", "_").lower()
      stub = bookings_pb2_grpc.BookingsStub(channel)
      responses = get_bookings(stub, userid)
      print(responses.message)
      if len(return_dict) != 0:
         return make_response(jsonify(return_dict), 200)
      return make_response(jsonify({"error":"Invalid user id"}), 400)


@app.route("/user/getMoviesInfo/<userid>", methods=['GET'])
def getMoviesInfo(userid):
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
