## Author:	Owen Cocjin
## Version:	0.1
## Date:	10/05/20
## Description:
##	Functions to process HTTP data given all data requested
## Note:

import requests as r

HTTPEND=[b'\r', b'\n', b'\r', b'\n']
MAGICSTR="/?url="

def splitURL(url):
	'''Split the domain from the page. Returns a tuple (domain, page)'''
	#Find the first slash after "://"
	slash=url.find('/', url.find("://")+3)
	#If no ending slash found (slash=-1), just return the given url
	if slash==-1:
		return url, '/'
	return url[:slash], url[slash:]

def makeLocalPath(req_path, root=''):
	'''Convert the client requested path into a local path'''
	if req_path=='/' or req_path[:2]=="/?":
		path="index.html"
	else:
		path=req_path
	return f"{root}/{path}"

def splitGET(data):
	'''Splits the GET data into a dictionary'''
	toRet={}
	for i in data.split('&'):
		arg, val=i.split('=')
		toRet[arg]=val
	return toRet

def main():
	pass


if __name__=="__main__":
	main()
