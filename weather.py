from multiprocessing import Process, Pipe
import socket

UDP_IP = "192.168.1.14"
UDP_PORT = 42069

def parse_udp(child_conn):  
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind((UDP_IP, UDP_PORT))
   while True:
      data, address = sock.recvfrom(4096)
      # TODO: parse and pack data received from ESP8266
      child_conn.send(data)
   sock.close()
   child_conn.close()

class Weather():
   def __init__(self):
      self.temp = 20
      self.humidity = 70
   
   def temp_fahrenheit_get(self):
      return round(self.temp * 1.8 + 32)
