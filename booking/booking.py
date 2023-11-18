from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import grpc
from concurrent import futures
import bookings_pb2
import bookings_pb2_grpc
import times_pb2_grpc
import times_pb2

from werkzeug.exceptions import NotFound


class BookingsServicer(bookings_pb2_grpc.BookingsServicer):

   def __init__(self):
      with open('{}/databases/bookings.json'.format("."), "r") as jsf:
         self.db = json.load(jsf)["bookings"]

   def GetAllBookings(self, request, context):
      for bookings in self.db:
         yield bookings_pb2.Booking(userid=bookings['userid'], dates=bookings['dates'])

   def GetBookingByUser(self, request, context):
      print('GetBookingByUser')
      list_dates = []
      for booking in self.db:
         if booking['userid'] == request.user:
            for one_date in booking['dates']:
               list_dates.append(one_date)
            yield bookings_pb2.Booking(userid=booking['userid'], dates=list_dates)

   def get_by_date(self, stub, date):
      movies_list = stub.GetMmoviesBydate(date)
      return movies_list

   def AddBookingByUser(self, request, context):
      with grpc.insecure_channel('localhost:3202') as channel:
         stub = times_pb2_grpc.TimeStub(channel)
         response = self.get_by_date(stub, request.date_booking)
         for movie in response.movies:
            if movie == request.movieid:
               for index_user in range(len(self.db)):
                  if self.db[index_user]["userid"] == request.userid:
                     one_booking = {
                        "date": request.date_booking.date, "movies": [request.movieid]
                     }
                     for index_date in range(len(self.db[index_user]['dates'])):
                        if self.db[index_user]['dates'][index_date]['date'] == request.date_booking.date:
                           if not (request.movieid in self.db[index_user]['dates'][index_date]['movies']):
                              self.db[index_user]['dates'][index_date]['movies'].append(request.movieid)
                              return bookings_pb2.Booking(userid=self.db[index_user]["userid"],
                                                          dates=self.db[index_user]["dates"])
                           context.abort(grpc.StatusCode.ALREADY_EXISTS, "le film existe déjà à cette date")
                        self.db[index_user]['dates'].append(one_booking)
                        return bookings_pb2.Booking(userid=self.db[index_user]["userid"],
                                                    dates=self.db[index_user]["dates"])
                  context.abort(grpc.StatusCode.ABORTED, "user introuvable")
               context.abort(grpc.StatusCode.ABORTED, "movie introuvable")
      context.abort(grpc.StatusCode.ABORTED, "erreur")



def serve():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   bookings_pb2_grpc.add_BookingsServicer_to_server(BookingsServicer(), server)
   server.add_insecure_port('127.0.0.1:3201')
   server.start()
   print("Server start")
   server.wait_for_termination()


app = Flask(__name__)

HOST = '0.0.0.0'
PORT = 3201

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# @app.route("/bookings", methods=['GET'])
# def get_json():
#    res = make_response(jsonify(bookings), 200)
#    return res
#
#
# @app.route("/bookings/<userid>", methods=['GET'])
# def get_booking_for_user(userid):
#    for booking in bookings:
#       if str(booking["userid"]) == str(userid):
#          return make_response(jsonify(booking), 200)
#    return make_response(jsonify({"error": "bad input parameter"}), 400)
#
#
# @app.route("/bookings/<userid>", methods=['POST'])
# def add_booking_byuser(userid):
#    req = request.get_json()
#    r = requests.get('http://192.168.1.12:3202/showmovies/' + req["date"])
#    if r.status_code == 200:
#       if req["movieid"] in r.json()["movies"]:
#          one_booking = {
#             "date": req["date"], "movies": [req["movieid"]]
#          }
#
#          for item in bookings:
#             if item["userid"] == userid:
#                if one_booking not in item["dates"]:
#                   item["dates"].append(one_booking)
#                   return make_response(jsonify(one_booking), 200)
#                return make_response(jsonify({"error": "an existing item already exists"}), 409)
#    return make_response(jsonify({"error": "cannot add booking"}), 400)


if __name__ == "__main__":
   serve()
