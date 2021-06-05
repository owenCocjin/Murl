##
## Author:  Owen Cocjin
## Version: 1.1
## Date:    2021.06.04
## Description:    Hold classes for socket server connections
## Notes:
##  - Need to add a timeout to recv OR figure out the total package length
## Update:
from typing import Tuple
from ProgMenu.progmenu import MENU
import socket
vprint=MENU.verboseSetup(['v', "verbose"])
class Proto():
	'''Absolute base class.
Used more as a template than anything.
All functions and variables here must be replaced/used (i.e. don't put your own raw bytes into another variable).'''
	def __init__(self):
		self.raw=b''

	def parse(_, raw):
		'''This function is absorbed by the Cli class and runs it by itself.
It uses this to convert raw data into a specific Proto class.
Normally this is used to create a repy class from a reply from the socket.
DO NOT reference any self vars here!'''
		return raw
	def compile(self):
		'''Compiles all self data to raw packet'''
		return self.raw
	def makeAnswer(self, data=None):
		'''Parses & adds data to self, then returns self.compile()'''
		return self.compile()

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new


class Dns(Proto):
	'''Manage DNS replies.
Only supports single query/answers at the moment.'''
	def __init__(self,
id=b"\xff\xff",
flags=b"\x81\xa0",
qsnrrs=b"\x00\x01\x00\x01\x00\x00\x00\x00",
*,
queries=None,
answers=None):
		Proto.__init__(self)
		self.id=id  #Transaction ID (2 bytes)
		self.flags=flags  #(2 bytes)
		self.qsnrrs=qsnrrs  #(4 bytes)
		self.queries=DnsPayload('ff.ff', 0x0001, 0x0001) if not queries else queries
		self.answers=None  #Set ttl to 1 to ensure it's an answer
		self.raw=b''
	def __str__(self):
		return f"""{self.id} | {self.flags} | {self.qsnrrs}
Queries: {self.queries}
Answers: {self.answers}"""

	def parse(_, data):
		'''Converts raw data to a Dns query object'''
		id=data[:2]
		flags=data[2:4]
		qsnrrs=data[4:12]
		#Get number of names
		pointer=12
		names=[]
		while data[pointer]!=0x00:
			names.append(data[(pointer+1):(data[pointer]+pointer+1)].decode())
			pointer+=data[pointer]+1
		name='.'.join(names)

		toret=Dns(id=id,\
flags=flags,\
qsnrrs=qsnrrs,\
queries=DnsPayload(name,data[-4:-2],data[-2:]))
		#Put an if that checks first bit of flags for 0==Query; 1==Answer
		return toret
	def compile(self):
		'''Convert all vars into a proper packet.
If answers is None, assumes this is a query'''
		self.raw=b''
		self.raw+=self.id
		self.raw+=self.flags
		self.raw+=self.qsnrrs
		self.raw+=self.queries.compile()
		if self.answers!=None:
			self.raw+=self.answers.compile()
		return self.raw
	def matchQtoA(self):
		'''Matches queries data to answers data'''
		self.answers=DnsPayload("match",\
self.queries.type_,\
self.queries.class_)

	def getId(self):
		return self.id
	def setId(self, new):
		self.id=new
	def getFlags(self):
		return self.flags
	def setFlags(self, new):
		self.flags=new
	def getQsnas(self):
		return self.qsnas
	def setQsnas(self, new):
		self.qsnas=new
	def getRrs(self):
		return self.rrs
	def setRrs(self, new):
		self.rrs=new
	def getQueries(self):
		return self.queries
	def setQueries(self, new):
		self.queries=new
	def getAnswers(self):
		return self.answers
	def setAnswers(self, new):
		self.answers=new
	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new

class DnsPayload():
	'''Data for queries and replies.
if name_=="match", will replace with bytecode 0xc00c in compilation.
Keep in mind this change ONLY applies to the return of compilation, which also affects self.raw'''
	def __init__(self, name_, type_, class_, ttl=0x00000000, addr="0.0.0.0"):
		'''CAUTION: If all of ttl, data_len, and addr are None, this is assumed to be a query instead of a reply!'''
		self.name_=name_  #str
		self.type_=type_  #2 bytes
		self.class_=class_  #2 bytes
		#v Only used by answer v
		self.ttl=ttl  #4 bytes
		self.addr=[int(i) for i in addr.split('.')]  #4 bytes
		self.addr_bytes=0
		self.addr2bytes()
		self.data_len=len(self.addr)  #2 bytes
		self.raw=b''
	def __str__(self):
		return f"{self.name_} | {self.type_} | {self.class_} \
({self.ttl} ; {self.addr} ; {self.data_len})"

	def getQuery(self):
		'''Returns a tuple of just (name, type, class)'''
		return (self.name_, self.type_, self.class_)
	def getAnswer(self):
		'''Returns a tuple of everything'''
		return (self.name_,\
self.type_,\
self.class_,\
self.ttl,\
self.data_len,\
self.addr_bytes)
	def compile(self):
		'''Compiles all data into self.raw'''
		self.raw=b''
		if self.name_=="match":
			self.raw+=b"\xc0\x0c"
		else:
			for n in self.name_.split('.'):
				length=hex(len(n))[2:]
				if len(length)%2:
					length=f"0{length}"
				self.raw+=bytes.fromhex(length)
				self.raw+=n.encode()
			self.raw+=b"\x00"
		self.raw+=self.type_
		self.raw+=self.class_
		if not self.isQuery():  #Answer
			self.raw+=self.ttl.to_bytes(4, "big")
			self.raw+=self.data_len.to_bytes(2, "big")
			self.raw+=self.addr_bytes.to_bytes(4, "big")
		return self.raw

	def isQuery(self):
		'''Returns True if a query, False if an answer'''
		if self.ttl+self.addr_bytes==0:
			return True
		return False
	def addr2bytes(self):
		self.addr_bytes=0
		for b in self.addr:
			self.addr_bytes<<=8
			self.addr_bytes+=b
		return self.addr_bytes

	def getName_(self):
		return self.name_
	def setName_(self, new):
		self.name_=new
	def getType_(self):
		return self.type_
	def setType_(self, new):
		self.type_=new
	def getClass_(self):
		return self.class_
	def setClass_(self, new):
		self.class_=new
	def getTtl(self):
		return self.ttl
	def setTtl(self, new):
		self.ttl=new
	def getData_len(self):
		return self.data_len
	def setData_len(self, new):
		self.data_len=new
	def getAddr(self):
		return self.addr
	def setAddr(self, new):
		'''Takes a str of and addr and converts to one int.
Ex input: "192.168.2.1" '''
		self.addr=[int(i) for i in new.split('.')]
		self.addr2bytes()
	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
	def getAddr_bytes(self):
		return self.addr_bytes
	def setAddr_bytes(self, new):
		self.addr_bytes=new


class SrvBase():
	def __init__(self, toru="UDP"):
		self.sock=None
		self.client=None
		self.toru=toru
		self.psize=1024
		self.byte_buff=b''
		self.req_buff=b''
		if self.toru.upper()=="UDP":
			self.recv=self._recvUDP
			self.bind=self._bindUDP
			self.send=self._sendUDP
		elif self.toru.upper()=="TCP":
			self.recv=self._recvTCP
			self.bind=self._bindTCP
			self.send=self._sendTCP
	def _recvUDP(self):
		self.req_buff, self.client=self.sock.recvfrom(self.psize)
		return self.req_buff
	def _recvTCP(self):
		self.sock.accept()
		self.client, self.req_buff=self.sock.recv(self.psize)
		return self.req_buff
	def _sendUDP(self):
		'''Sends whatever is in byte_buff'''
		self.sock.sendto(self.byte_buff, self.client)
	def _sendTCP(self):
		self.sock.send(self.byte_buff)
	def _bindUDP(self):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(self.host)
		return self.sock
	def _bindTCP(self):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(self.host)
		self.sock.listen()
	def reset(self):
		self.sock.close()
		return self.bind()

	def getReq_buff(self):
		return self.req_buff
	def setReq_buff(self, new):
		self.req_buff=new


class Srv(SrvBase):
	'''Manages server connection'''
	protos={"Dns":Dns}
	def __init__(self, host, proto="Dns", proto_args=None, toru="UDP"):
		SrvBase.__init__(self, toru)
		self.host=host
		self.proto_name=proto
		self.proto_args=proto_args
		if self.proto_args==None:
			self.proto=Srv.protos[self.proto_name]()
		else:
			self.proto=Srv.protos[self.proto_name](*self.proto_args)
		self.sock=None
		self.request=None  #Received proto
		self.toru=toru
		self.byte_buff=b''
		self.client=None
		self.psize=1024  #Size of recv
		self.bind()

	def getHost(self):
		return self.host
	def setHost(self, new):
		self.host=new
	def getProto_name(self):
		return self.proto_name
	def setProto_name(self, new):
		self.proto_name=new
	def getProto_args(self):
		return self.proto_args
	def setProto_args(self, new):
		self.proto_args=new
	def getSock(self):
		return self.sock
	def setSock(self, new):
		self.sock=new
	def getToru(self):
		return self.toru
	def setToru(self, new):
		self.toru=new
	def getByte_buff(self):
		return self.byte_buff
	def setByte_buff(self, new):
		self.byte_buff=new
	def getPsize(self):
		return self.psize
	def setPsize(self, new):
		self.psize=new
