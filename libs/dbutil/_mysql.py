# -*- coding:utf-8 -*-
import re
try:
	import mysql.connector as _myconnector
except ImportError,e:
	print e
	import sys
	import os
	path=os.path.dirname(sys.executable)
	print path
	sys.path.insert(0,os.path.join(path,"Lib\site-packages"))

	print sys.path
	import mysql.connector as _myconnector
	print 2,e

"""
mysql operator functions

"""

__all__=["get_connect","MysqlServer"]



def get_connect(host,port,database):

	if host and port and database:
		mysqlServer=MysqlServer(host,port,database)
		return mysqlServer.connect()
	else:
		raise ValueError("connect to %s fail." %(server,))




class MysqlServer(object):
	
	def __init__(self,host,port,database):
		self._host=host
		self._database=database
		self._port=port
		self._login_timeout=3
		self._charset="utf8"
		#self.__conn=None

	def connect(self):
		try:
			uid="us_shi_jy"
			pwd="qbus+0901qpalz,"
			print self._host,self._database,self._port
			self._conn= _myconnector.connector.connect(user=uid, password=pwd,
                              host=self._host,
                              port=self._port,
                              database=self._database,
                              charset=self._charset,
                              connection_timeout =self._login_timeout)
		except Exception,e:
			raise ValueError("connect to {0} fail,{1}".format(self._host,e))

		return self

	def exec_query(self,sql,*args):
		cursor=self._conn.cursor()
		cursor.execute(sql,args)
		ret= cursor.fetchall()
		cursor.close()
		return ret

	def exec_query_dict(self,sql,*args):
		cursor=self._conn.cursor(dictionary=True)
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



if __name__ == '__main__':
	sqlmonitor=get_connect("SQLMonitor.db.sh.ctripcorp.com",55944,"sqlmonitordb")
	data=sqlmonitor.exec_query("select machine_name from _del_cf_database limit 10","configdb")
	print data
	sqlmonitor.close()