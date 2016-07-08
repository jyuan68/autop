# -*- coding:utf-8 -*-

import unittest
from . import SqlTemplate

class test_SqlTemplate(unittest.TestCase): 
	##初始化工作 
	def setUp(self): 
		self.temp=SqlTemplate("alter database $name set partner $enable")
	#退出清理工作 
	def tearDown(self): 
		pass
	#具体的测试用例，一定要以test开头 
	def testsubstitute(self): 
		self.assertEqual(self.temp.substitute({"name":"paybasedb","enable":"on"}), "alter database paybasedb set partner on", 'test substitute fail>1.') 
		self.assertEqual(self.temp.substitute({"name":"paybasedb","enable":"off"}), "alter database paybasedb set partner off", 'test substitute fail>2.') 
		self.assertEqual(self.temp.substitute({"name":"paybasedb","failover":"force_failover_allow_data_loss"}), "alter database paybasedb set partner force_failover_allow_data_loss", 'test substitute fail>3.') 
if __name__ =='__main__': 
	unittest.main()
