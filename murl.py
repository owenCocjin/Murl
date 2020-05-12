#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	0.1
## Date:	10/05/20
## Description:
##	Redirect a user's link to any page as if the page was being hosted on your machine
## Note:

import requests, socket, time, asyncio
from processing import splitURL, splitHTTP, splitGET, parseData
from requesting import handle_session
#from bs4 import BeautifulSoup
HOST='0.0.0.0'
PORT=80

async def main():
	client_map={}  #Keep track of which IP is asking for what domain
	serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#Check for sudo if port below 1024
	try:
		serv.bind((HOST, PORT))
	except PermissionError as e:
		print(f"[|X:main:bind]: {PORT} is well-known. Run script as root!")
		exit(1)
	serv.listen(5)
	print(f"SERVER:\t{HOST}:{PORT}")

	#Start accepting connections
	while True:
		#Process HTTP request from client
		cli_sock, cli_addr=serv.accept()  #Accept connection
		print(f"\nGot a request from {cli_addr[0]}:{cli_addr[1]}!")

		await handle_session(cli_sock, cli_addr, client_map)

		#Close socket
		cli_sock.close()
		print(f"Closed connection with {cli_addr[0]}:{cli_addr[1]}!")

if __name__=="__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt as e:
		print("\n[|X]: Manual Close!")
