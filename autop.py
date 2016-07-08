# -*- coding:utf-8 -*-

import os
import sys

import string
from collections import namedtuple
try:
	os.path.join(__path__, 'libs')
except Exception, e:
	__path__=os.getcwd()
libs_path = os.path.join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from dbutil import mssql


class BriefObject(dict):
	def __init__(self, *args, **kwargs):
		 super(Vardata, self).__init__(*args, **kwargs)
		 self.__dict__.update(kwargs)

def transfer_to_briefobject(datatable):
	return [BriefObject(rowset) for rowset in datatable]



class TemplateList:
	def __init__(self)
		self.tls=[]

	def push(self,command):
		self.tls.push(command)

	def insert(self,locate,command):
		self.tls.insert(locate,command)

	def __getitem__(self,index):
		return self.tls[index]

	def __setitem__(self,index,data):
		if isinstance(data,Command):
			self.tls[index]=data
		else:
			raise TypeError("*data %s type is error" % (data,))



class App:
	def __init__(self,checklist):
		self.stack_buttom=None
		self.stack_top=self.stack_buttom
		self.templateList=TemplateList

	def init_content(self):
		pass
	def destory_content(self):
		pass
	def run(self):
		self.init_content()
		for cmd in self.templateList:
			frame=CStackFrame(cmd)
			frame.back=self.stack_buttom
			self.stack_top=frame
			if self.stack_buttom:
				self.stack_buttom=frame

			frame.run()

		self.destory_content()

class CStackFrame:
	def __init__(self,cmdobj):
		self._command=cmdobj
		self._global_variables={}
		self._local_variables={"servername":"clsfltorder14","dns":"fltorder.db.ctripcorp.com","port":55944,"host":dataset}
		self._back=None

	def run(self):
		#update variable
		self.command.run()

	def set_local_variable(self,key,value):
		self._local_variables[key]value

	@property
	def local_variables(self):
	    return self._local_variables
	

	def set_global_variable(self,key,value):
		self._global_variables[key]value

	@property
	def global_variables(self):
	    return self._global_variables
	


class VariablesCollections:
	def __init__(self,name,value,isreadonly=False):
		self.name=name
		self._value=value
		self._readonly=isreadonly

	@property
	def readonly(self):
	   return self._readonly

	@property
	def value(self):
	   return self._value

	def __getattr__(self,attrname):
		pass






class Command(object):
	def __init__(self):
		pass

class ImportCommand(Command):
	def __init__(self,module):
		self._module=module
	def text(self):
		return "import %s" % (module)



class ForeachCommand(Command):
	template="""
		for d in datalist:
			cmd(d)
	"""

	def __init__(self,datalist,cmd):
		self.data=datalist

	def run(self,frame):
		pass

	def __str__(self):
		pass

	def __repr__(self):
		self.__str__()

class MapCommand(Command):
	template="""
		for d in datalist:
			cmd(d)
	"""

	def __init__(self,datalist,template):
		self.data=datalist
		self.template=template
	def run(self,frame):
		r=[]
		for d in datalist:
			t=string.Template(template)
			t.substitute(d.transfer)
			t.substutite(frame.lobalVariables)
			t.substutite(frame.globalVariables)


	def __str__(self):
		pass

	def __repr__(self):
		self.__str__()
class ReduceCommand(Command):
	template="""
		for d in datalist:
			cmd(d)
	"""

	def __init__(self,datalist,cmd):
		self.data=datalist

	def run(self,frame):
		pass

	def __str__(self):
		pass

	def __repr__(self):
		self.__str__()
		pass

#  $service.hostname,$service.port,$service.machine_name



class ScriptHeader:
	
	def __init__(self):
		self._template="""
# -*- coding:utf-8 -*-
import sys
import os

try:
	os.path.join(__path__, 'libs')
except Exception, e:
	__path__=os.getcwd()
libs_path = os.path.join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
from dbutil import mssql
	"""

	def text(self):
		return self._template

class ScriptMain:
	def __init__(self):
		self._template="""
if __name__ =='__main__':
	main()
	"""
		pass

	def text(self):
		return self._template


if __name__ == '__main__':

	sqlcmd=SqlQueryCommand("sqlperformance.db.sh.ctripcorp.com,55944","TraceDB","select name from sys.tables(nolock) where name=%s","AutoCollectNetworkInterfaceQuery")
	header=ScriptHeader()
	main=ScriptMain()

	print header
	print main
	print sqlcmd
