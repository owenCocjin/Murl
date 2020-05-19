## Author:	Owen Cocjin
## Version:	0.1
## Date:	11/05/20
## Description:
##	Create a session to a website
## Note:
import requests

async def handle_session():
	'''Create a session with the target URL and maintain until the target client is done'''
	#Create request session
	sess=requests.Session()
