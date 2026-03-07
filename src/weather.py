from multiprocessing import Process, Pipe
import socket

UDP_IP = "192.168.4.140"
UDP_PORT = 42069

def relay_udp_data(child_conn):  
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind((UDP_IP, UDP_PORT))
   while True:
      rawData, addr = sock.recvfrom(4096)
      try:
         child_conn.send(parse_msg(rawData))
      except Exception as e:
         print(e)
   sock.close()
   child_conn.close()

def parse_msg(udpData):
   humidityString = str(udpData[0]) + '.' + str(udpData[1])
   tempString = str(udpData[2]) + '.' + str(udpData[3])
   fillLevelString = str(udpData[4])
   humidity = float(humidityString)
   temp = float(tempString)
   fillLevel = float(fillLevelString)
   return (humidity, temp, fillLevel)


class Weather():
   def __init__(self):
      self.temp = 0
      self.humidity = 0
      self.fillLevel = 0
   
   def temp_fahrenheit_get(self):
      return round(self.temp * 1.8 + 32)
