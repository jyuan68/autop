# -*- coding:utf-8 -*-
import string


class SqlTemplate(string.Template):  
    """docstring for sql
    select * from $tablename

    select '$tablename'
    """  
    delimiter = '$'  

    def __init__(self,template,strdelimiter='$'):
    	delimiter=strdelimiter
    	super(SqlTemplate,self).__init__(template)

