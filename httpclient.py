#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):
    
   # print ("here in HTTPClient")
    def connect(self, host, port):
        # use sockets!
       # print("here in connect")
      #  print ("host:",host)
      #  print ("port:",port)
        
        if port == None:
            port = 80
        connect_with = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_with.connect((host,port))
        return connect_with

    def get_code(self, data):
        #print("here in get_code")
       # print data
        return int(data.split(' ',2)[1])

    def get_headers(self,data):
       # print("here in get_headers")
        #print data
        return data.split('\r\n\r\n')[0]


    def get_body(self, data):
        #print("here in get_body")
        
        #print data
        return data.split('\r\n\r\n',2)[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):   
        #https://docs.python.org/2/library/urlparse.html 1/25/2016
        o=urlparse(url)
        connect_with = self.connect(o.hostname,o.port)
        connect_with.send("GET "+o.path+" HTTP/1.1\r\nHost: "+o.hostname+"\r\nAccept: */*\r\nConnection: close\r\n\r\n")
        receive = self.recvall(connect_with)
        code = self.get_code(receive)
        body = self.get_body(receive)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        if args == None:
            Poststring = ""
        else:
            Poststring = urllib.urlencode(args)
        
        o=urlparse(url)
        connect_with = self.connect(o.hostname,o.port)
        connect_with.send("POST "+o.path+" HTTP/1.1\r\nHost: "+o.hostname+"\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: "+str(len(Poststring))+"\r\n\r\n"+Poststring+"\r\n")
        receive = self.recvall(connect_with)
        code = self.get_code(receive)
        body = self.get_body(receive)
        return HTTPResponse(code, body)

    def command(self, command, url, args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
