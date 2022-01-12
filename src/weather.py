from multiprocessing import Process, Pipe
import socket, re

UDP_IP = "192.168.1.14"
UDP_PORT = 42069

def parse_udp(child_conn):  
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind((UDP_IP, UDP_PORT))
   while True:
      rawData, address = sock.recvfrom(4096)
      try:
         data = int(rawData)
         dataStrings = re.findall(r'\d{1,2}', str(data))
         humidityString = dataStrings[0] + '.' + dataStrings[1]
         tempString = dataStrings[2] + '.' + dataStrings[3]
         humidity = float(humidityString)
         temp = float(tempString)
         child_conn.send((humidity, temp))
      except Exception as e:
         print(e)
   sock.close()
   child_conn.close()

class Weather():
   def __init__(self):
      self.temp = 0
      self.humidity = 0
   
   def temp_fahrenheit_get(self):
      return round(self.temp * 1.8 + 32)
