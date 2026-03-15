from flask import Flask, render_template, jsonify
from multiprocessing import Process, Pipe
import socket, weather, server_thread

DATA_UPDATE_TIMEOUT = 120 # Seconds (2 minutes)
WeatherObject = weather.Weather()

def main():
   start_server()
   parent_conn, child_conn = Pipe()
   weather_process = Process(target=weather.relay_udp_data, args=(child_conn, ))
   weather_process.start()
   while True:
      try:
         if (parent_conn.poll(DATA_UPDATE_TIMEOUT)):
            weather_data = parent_conn.recv()
            WeatherObject.humidity = round(weather_data[0])
            WeatherObject.temp = weather_data[1]
            WeatherObject.fillLevel = weather_data[2]
         else:
            # No weather data was received before timeout, set weather data to N/A
            WeatherObject.humidity = "---"
            WeatherObject.temp = "---"
            WeatherObject.fillLevel = "---"
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
      temperature = WeatherObject.temp_fahrenheit_get()
      humidity = WeatherObject.humidity
      fillLevel = WeatherObject.fillLevel
      return jsonify(temperature = temperature, humidity = humidity, fillLevel = fillLevel)

   server = server_thread.ServerThread(app)
   server.start()
   print('server started')

if __name__ == '__main__':
   main()
