## Author:	Owen Cocjin
## Version:	0.1
## Date:	11/05/20
## Description:
##	Create a session to a website
## Note:
import asyncio, requests
from processing import splitHTTP, splitURL, parseData

MAGICSTR="/?url="

async def handle_session(sock, addr, client_map):
	'''Fetch and return data to client'''
	data=parseData(sock, addr)

	#First connection from IP
	if data["page"][:6]==MAGICSTR:
		target_domain, target_page=splitURL(data["page"][6:])
		client_map[addr[0]]=target_domain
	else:  #There SHOULD be an ip-domain in the map
		target_domain, target_page=client_map[addr[0]], data["page"]

	print(f"target: {target_domain}{target_page}")
	req=requests.get(f"{target_domain}{target_page}", headers={"User-Agent":data["user-agent"]})
	sock.send(req.content)

	return target_domain, target_page
