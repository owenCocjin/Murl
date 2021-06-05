#!/bin/python3
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.04
## Description:    Main code for Murl
## Notes:
##   - Make sure you setup the correct firewall rules to allow UDP connection:
##   - iptables -A INPUT -p udp --dport 53 -j ACCEPT
##   - iptables -A OUTPUT -p udp --sport 53 -j ACCEPT
##   - Would prefer if this page is what did most of the processing rather than in the Srv class
##   - It has become quite cluttered in that class
import connection as con
from ProgMenu.progmenu import MENU
vprint=MENU.verboseSetup(['v', "verbose"])
def main():
	print("[|X:main]: Setting up DNS server...")
	srv=con.Srv(("0.0.0.0", 53), "Dns")  #Creates a default DNS in srv.proto
	srv.bind()
	while True:
		print("\n[|X:main]: Stepping...")
		srv.recv()
		srv.request=srv.proto.parse(srv.getReq_buff())
		vprint(f"[|X:main]: Received from {srv.client}: ")
		vprint(srv.request)
		#Copy relevant data to srv.proto
		srv.proto.id=srv.request.getId()
		srv.proto.queries=srv.request.getQueries()
		#Construct answer
		srv.proto.matchQtoA()
		srv.proto.answers.setTtl(86400)
		srv.proto.answers.setAddr("155.138.133.28")
		srv.byte_buff=srv.proto.compile()
		print("[|X:main]: Sending reply...")
		vprint(srv.proto)
		print(srv.getByte_buff())
		srv.send()
		print("[|X:main]: Done!")

def buildTypeA(self, sock):
	'''Builds a type A answer (normal IPv4 host)'''

def buildTypeAAAA(self, sock):
	'''Builds a type AAAA answer (IPv6)'''
	


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\r\033[K", end='')
	except PermissionError as e:
		print(f"[|X:main:PermissionError]: {e}")
