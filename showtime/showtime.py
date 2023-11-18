from flask import Flask, render_template, request, jsonify, make_response
import json
import grpc
from concurrent import futures
import times_pb2
import times_pb2_grpc


class TimeServicer(times_pb2_grpc.TimeServicer):

   def __init__(self):
      with open('{}/databases/times.json'.format("."), "r") as jsf:
         self.db = json.load(jsf)["schedule"]

   def GetAllShowtimes(self, request, context):
      for time in self.db:
         yield times_pb2.ShowTime(date=time['date'], movies=time['movies'])

   def GetMmoviesBydate(self, request, context):
      for time in self.db:
         if time['date'] == request.date:
            return times_pb2.ShowTime(date=time['date'], movies=time['movies'])
      # Gérer le cas où aucune correspondance n'a été trouvée ici.


from werkzeug.exceptions import NotFound
app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# @app.route("/showtimes", methods=['GET'])
# def get_schedule():
#    res = make_response(jsonify(schedule), 200)
#    return res
#
# @app.route("/showmovies/<date>", methods=['GET'])
# def get_movies_bydate(date):
#    for sch in schedule:
#       if str(sch["date"]) == str(date):
#         return make_response(jsonify(sch), 200)
#    return make_response(jsonify({"error":"bad input parameter"}),400)

def serve():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   times_pb2_grpc.add_TimeServicer_to_server(TimeServicer(), server)
   server.add_insecure_port('127.0.0.1:3202')
   server.start()
   print("Server start")
   server.wait_for_termination()


if __name__ == '__main__':
 serve()