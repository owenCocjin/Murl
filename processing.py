## Author:	Owen Cocjin
## Version:	0.1
## Date:	10/05/20
## Description:
##	Functions to process HTTP data given all data requested
## Note:

import requests as r

HTTPEND=[b'\r', b'\n', b'\r', b'\n']
MAGICSTR="/?url="

def parseData(cli_sock, cli_addr):
	'''Read HTTP request data from cli_socket'''
	target_domain=None
	httpFrame=['', '', '', '']
	recv_info=''

	#Read 1 bit at a time into the httpFrame
	while httpFrame!=HTTPEND:
		httpFrame=[httpFrame[i+1] for i in range(3)]+[cli_sock.recv(1)]  #Move httpFrame by 1, replace last bit
		recv_info+=httpFrame[-1].decode("utf-8")
	recv_info=splitHTTP(recv_info)
	print(recv_info)
	print(f'''GET INFO:
\t{"Host:":<15}{recv_info["host"]}
\t{"Method:":<15}{recv_info["method"]}
\t{"Page:":<15}{recv_info["page"]}
\t{"Connection:":<15}{recv_info["connection"]}
\t{"User-Agent:":<15}{recv_info["user-agent"]}''')
	try:
		print(f'''\tReferer:\t{recv_info["referer"]}''')
	except:
		pass

	return recv_info

def splitHTTP(data):
	'''Splits http request data into different components'''
	data=data.strip('\r\n\r\n').split('\r\n')
	toRet={}.fromkeys(["method", "page", "version"], None)
	#First line is unique
	for i, j in zip(toRet, data[0].split(' ')):
		toRet[i]=j
	#All other lines follow Arg: data
	for d in data[1:]:
		colon=d.find(':')
		arg, val=d[:colon], d[colon+1:].strip()
		toRet[arg.lower()]=val
	return toRet

def splitURL(url):
	'''Split the domain from the page'''
	#Find the first slash after "://"
	slash=url.find('/', url.find("://")+3)
	#If no ending slash found (slash=-1), just return the given url
	if slash==-1:
		return url, '/'
	return url[:slash], url[slash:]

def splitGET(data):
	'''Splits the GET data into a dictionary'''
	toRet={}
	for i in data.split('&'):
		arg, val=i.split('=')
		toRet[arg]=val
	return toRet


def main():
	print("Testing HTTPRequest class!")
	url_d, url_p=splitURL("https://postman-echo.com/post")
	req=r.post(f"{url_d}{url_p}", params={"getparam":"works"}, data={"postdata":"correct"})
	print(f"{req} <- {url_d}{url_p}")
	print(req.content)
	exit()
	print(splitHTTP('''GET / HTTP/1.1\r
Host: localhost\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Connection: keep-alive\r
Upgrade-Insecure-Requests: 1\r
Cache-Control: max-age=0\r
'''))

if __name__=="__main__":
	main()
