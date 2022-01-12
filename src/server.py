from flask import Flask, render_template, jsonify
from multiprocessing import Process, Pipe
import socket, weather, server_thread

weather_object = weather.Weather()

def main():
   start_server()
   parent_conn, child_conn = Pipe()
   weather_process = Process(target=weather.parse_udp, args=(child_conn, ))
   weather_process.start()
   while True:
      try:
         weather_data = parent_conn.recv() # TODO: deduce clever way to pack and parse weather data from weather process to server
         weather_object.humidity = round(weather_data[0])
         weather_object.temp = weather_data[1]
      except Exception as e:
         print(e)
   stop_server()

def stop_server():
   global server
   server.shutdown()
   print("server shutdown")

def start_server():
   global server
   app = Flask(__name__)

   @app.route('/')
   def index(): 
      return render_template('index.html')

   @app.route('/_data', methods= ['GET'])
   def data():
      temperature = weather_object.temp_fahrenheit_get()
      humidity = weather_object.humidity
      return jsonify(temperature = temperature, humidity = humidity)

   server = server_thread.ServerThread(app)
   server.start()
   print('server started')

if __name__ == '__main__':
   main()
