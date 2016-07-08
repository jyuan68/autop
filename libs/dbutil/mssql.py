# -*- coding:utf-8 -*-
import re
import pymssql
import logging
from argparse import ArgumentParser

"""
database operator functions

"""

__all__=["get_connect","MssqlServer","MsDnsParser"]

class MsDnsParser(object):
	pattern_mssql_dns=r"(?P<servername>\D+\w*)\.db.(?P<env>sh|sh2|sh3|fat|uat|lpt)?(?(env)\.)(?P<domoin>qa.nt.ctripcorp|ctripcorp|ctriptravel){1}\.com,(?P<port>\d+)"

	def __init__(self):
		self.pattern=re.compile(MsDnsParser.pattern_mssql_dns,re.I)
		
	def isvalid(self,dns):
		m=self.pattern.match(dns)
		if m:
			return True
		else:
			return False
	
	def parser(self,dns):
		m=self.pattern.match(dns)
		if m:
			return m.groups()
		else:
			return None
	def parser_dict(self,dns):
		m=self.pattern.match(dns)
		if m:
			return m.groupdict()
		else:
			return None

def parse_mssql_connection_string(dns):
	dnsparser=MsDnsParser()
	dnsobj= dnsparser.parser_dict(dns)
	#print dnsobj
	if dnsobj:
		dns1=p=dns.partition(",")[0]
		env=dnsobj["env"]
		port=dnsobj["port"]
		return (dns1,env,port)
	else:
		raise ValueError("Dns format is error:%s" % (dns))

def get_connect(server,database="master"):
	dns,env,port=parse_mssql_connection_string(server)

	if dns and port:
		mssqlserver=MssqlServer(dns,database,port)
		if env.lower() in ["fat","lpt","uat"]:
			return mssqlserver.connect_win()
		else:
			return mssqlserver.connect()
	else:
		raise ValueError("connect to %s fail." %(server,))




class MssqlServer(object):
	
	def __init__(self,server,database,port):
		self._servername=server
		self._database=database
		self._port=port
		self._login_timeout=3
		self._charset="UTF-8"
		#self.__conn=None

	def connect(self):
		try:
			uid=""
			pwd=""
			print self._servername,self._database,self._port
			self._conn= pymssql.connect(server=self._servername,database=self._database,port=self._port,user=uid,password=pwd,login_timeout=self._login_timeout,charset=self._charset)
		except Exception,e:
			raise ValueError("connect to {0} fail,{1}".format(self._servername,e))

		return self

	def connect_win(self):
		try:
			self._conn= pymssql.connect(server=self._servername,database=self._database,port=self._port,login_timeout=self._login_timeout,charset=self._charset)
		except Exception,e:
			raise ValueError("connect to {0} fail,{1}".format(self._servername,e))

		return self

	def exec_query(self,sql,*args):
		cursor=self._conn.cursor()
		cursor.execute(sql,args)
		ret= cursor.fetchall()
		cursor.close()
		return ret

	def exec_query_dict(self,sql,*args):
		cursor=self._conn.cursor(as_dict=True)
		cursor.execute(sql,args)
		ret= cursor.fetchall()
		cursor.close()
		return ret

	def exec_update(self,sql,*args):
		cursor=self._conn.cursor()
		cursor.execute(sql,args)
		self._conn.commit()
		cursor.close()

	def exec_updatemany(self,sql,datalist):
		cursor=self._conn.cursor()
		cursor.executemany(sql,datalist)
		self._conn.commit()
		cursor.close()

	def close(self):
		self._conn.close()

	def __del__(self):
		if hasattr(self,"_conn"):
			print 'del'
			self._conn.close()


import unittest

class MssqlServerTest(unittest.TestCase):
	def setup(self):
		self.sqlperformance=get_connect("sqlperformance.db.sh.ctripcorp.com,55944")

	def teardown(self):
		self.sqlperformance.close()

	def testexec_query(self):
		self.assertTupleEqual(self.sqlperformance.exec_query("select name from sys.databases where name =%s","configdb"))

	def testexec_query_dict(self):
		pass

	def testexec_update(self):
		pass

	def testexec_updatemany(self):
		pass


if __name__ == '__main__':
	#sqlperformance=get_connect("sqlperformance.db.sh.ctripcorp.com,55944")
	#data=sqlperformance.exec_query("select name from sys.databases where name =%s","configdb")
	#print data
	#sqlperformance.close()


	#sqlperformance=get_connect("sqlperformance.db.sh.ctripcorp.com,55944","[CheckSPDB]")
	##data=sqlperformance.exec_update("create table __test(id int,data varchar(100))")
	#sqlperformance.exec_update("insert into __test(id,data) select %d,%s",10,"newid()")
	#a=[(11,"a"),(12,"b"),(13,"c")]
	#sqlperformance.exec_updatemany("insert into __test(id,data) values( %d,%s)",a)
	#sqlperformance.close()


	#VisaProduct=get_connect("VisaProduct.db.uat.qa.nt.ctripcorp.com,55777")
	#data=VisaProduct.exec_query("select name from sys.databases ")
	#print data
	#VisaProduct.close()


	#parser=ArgumentParser()
	#parser.add_argument("-v",action="store_true",dest="version",help='get the version of this program')
	#parser.add_argument("-s",action="store_true",dest="text",help='search')
	#parser.add_argument("-t",action="store",dest="text2",help='text')
	#parser.add_argument("search",action="store",help='search something')
	#import sys
	#print sys.argv[1:]
	#a= parser.parse_args(sys.argv[1:])
	#print '-'*30
	#print a
	#if a.search:
	#	while True:
	#		readline


	from pylsy import pylsytable

	attributes = ["name", "age"]
	table = pylsytable(attributes)

	age = [1, 2,3,4,5,6,]
	table.add_data("age", age)

	new_names = [
	        "ZAdsadminSlave.mysql.sh.ctriptravel.com,55944",
	        "ZipCode.db.uat.qa.nt.ctripcorp.com,55777",
	        "ZipCode.db.uat.qa.nt.ctripcorp.com,55777",
	        "ZipCode.db.uat.qa.nt.ctripcorp.com,55777"
	]
	table.add_data("name", new_names)

	while True:
		s=raw_input("search>")
		print s
		print table.__str__()
