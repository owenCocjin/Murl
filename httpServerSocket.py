#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	0.2
## Date:	15/05/20
## Description:
##	Functions to handle the target client -> Murl server connection
## Note:

import os.path, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from processing import makeLocalPath

HOST='127.0.0.1'
PORT=80

class RequestHandler(BaseHTTPRequestHandler):
	#Set class-wide variables
	protocol_version="HTTP/1.1"
	server_version="Murl/0.1"
	sys_version=""
	timeout=3

	def __init__(self, request, client_address, server):
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
		#print(f"[|X:RequestHandler:__init__]: local_path={self.local_path}")

	def sendDefaultHeaders(self, filename=None, *, end=None):
		'''Send required/common headers'''
		if filename:
			_response=200
			_content_length=os.path.getsize(filename)
		else:
			_response=204
			_content_length=0

		print(f"CONTENT-LENGTH: {_content_length}")
		print(f"CLIENT: {self.client_address}")

		self.send_response(_response)
		self.send_header("Connection", "keep-alive")
		self.send_header("Content-Length", _content_length)
		self.send_header("Keep-Alive", "timeout=5, max=10")

		#Send end_headers if end is passed
		if end:
			self.end_headers()

	def do_GET(self):
		print(f"Headers: {self.headers}")
		local_path=makeLocalPath(self.path, root="Home")

		try:
			with open(local_path, "br") as p:
				self.sendDefaultHeaders(local_path, end=True)
				self.wfile.write(p.read())
		except Exception as e:
			self.send_response(404)
			self.send_header("Content-Length", len(str(e)))
			self.end_headers()
			self.wfile.write(str(e).encode())

	def do_HEAD(self):
		self.sendDefaultHeaders(end=True)

def test():
	serv_addr=(HOST, PORT)
	httpd=HTTPServer(serv_addr, RequestHandler)
	httpd.serve_forever()
	self.wfile.write(b'')


if __name__=="__main__":
	try:
		test()
	except KeyboardInterrupt:
		print("\r[|X]: Manual Close")
