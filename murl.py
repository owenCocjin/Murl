#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	0.1
## Date:	15/05/20
## Description:
##	Redirect a user's link to any page as if the page was being hosted on your machine
## Note:

from httpServerSocket import RequestHandler
from http.server import ThreadingHTTPServer, HTTPServer

HOST='10.0.0.94'
PORT=80

def main():
	print(f"[|X:Murl]: Starting server ({HOST}:{PORT})!")
	serv_addr=(HOST, PORT)
	httpd=ThreadingHTTPServer(serv_addr, RequestHandler)
	while True:
		httpd.serve_forever()


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt as e:
		print("\r\033[K[|X]: Manual Close!")
