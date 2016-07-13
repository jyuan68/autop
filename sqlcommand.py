# -*- coding:utf-8 -*-

import re
import os

class ParamError(Exception):
    def __init__(self,msg):
        super(ParamError,self).__init__(msg)


def parse_param_config(strconfig):
    sep=os.linesep
    vardict={}
    l=strconfig.splitlines()
    multi_lines_cmd=[]
    variable_name=''
    length=len(l)
    for i,line in enumerate(l):
        line=line.lstrip()
        if line.startswith("$"):
            if variable_name:
                vardict[variable_name]=(sep.join(multi_lines_cmd)).lstrip()
                del multi_lines_cmd[:]
                variable_name=''
            try:
                variable_name,value=line.split("=")
                multi_lines_cmd.append(str(value))
            except ValueError, e:
                raise ValueError("line %d,%s" %(i,line,))
            
        else:
            multi_lines_cmd.append(line)
    if variable_name:
        vardict[variable_name]=(sep.join(multi_lines_cmd)).lstrip()
        del multi_lines_cmd[:]
        variable_name=''
    return vardict


def substutite_sql_string(source,**kwds):
    """
    example:
        select '$serviceobj.servername','$serviceobj.port',* from $dbname.dbo.tables(nolock)
    """
    length=len(source)
    def next_token(start):
        while start<length:
            c=source[i]
            if not ("A"<=c<="Z" or "a"<=c<="z" or "0"<=c<="9"):
                if c==".":


        else:

    def get_variable_value_by_name():
        pass
    data_list=[]
    i=0
    while i<length:
        c=source[i]
        if c=="$":
            i,var_identity=next_token(i+1)
            data_list.append("")
            data_list.append(get_variable_value_by_name(var_identity))
        i=i+1
    return ''.join(data_list)

class Command(object):
    def __init__(self):
        pass

class SqlCommand(Command):
    """
    $sql 必填参数，可执行的sql语句
    $dns 可选参数，指执行sql的目标服务器，该变量可继承
    $port 可选参数，当$dns是域名或者IP时，那么一定要提供$port，该变量可继承
    $return 可选参数，临时存储查询结果集时，指定结果集的名称

    example:
        $sql=select name,object_id 
        from sys.databases(nolock)
        $dns=fltorder.db.ctripcorp.com,55944
        $return=tableinfo
    """
    options_fix=["$sql"]
    options_option=["$dns","$port","$return","$db"]
    
    def __init__(self,str_config):
        self.connect_string=""
        self.db=""
        self.has_return_set=False
        self.config_option=parse_param_config(str_config)
        self._check_config()
    def _check_config(self):
        cf=self.config_option
        print cf
        for option in SqlCommand.options_fix:
            try:
                _ov=cf[option]
            except KeyError:
                raise ParamError("must provide parameter %s" % (option,))

        if "$dns" in cf:
            _ov=cf["$dns"]
            is_mssql= self._is_mssql_connect_string(_ov)
            
            if not is_mssql:
                print 1
                if self._is_dns(_ov) or self._is_ip(_ov):
                    if "$port" not in cf :
                        raise ParamError("lack the parameter $port")
                    else:
                        port=0
                        try:
                            port=int(cf["$port"])
                        except:
                            raise ParamError("$port must be a integer")
                        self.connect_string="%s,%d" % (_ov,port)
                else:
                    raise ParamError("$dns ( %s ) is error" % (_ov,))
            else:
                self.connect_string=_ov
        if not "$db" in cf:
            self.db=cf["$db"]="master"
        if "$return" in cf:
            self.has_return_set=True

    def _is_dns(self,dns):
        pattern_dns=r"(?P<servername>\D+\w*)\.db.(?P<env>sh|sh2|sh3|fat|uat|lpt)?(?(env)\.)(?P<domoin>qa.nt.ctripcorp|ctripcorp|ctriptravel){1}\.com"
        pattern=re.compile(pattern_dns,re.I)
        m=pattern.match(dns)
        if m:
            return True
        else:
            return False
    def _is_ip(self,ip):
        pattern_ip=r"(\d{1,3})\.(\d{1,3}).(\d{1,3})\.(\d{1,3})"
        pattern=re.compile(pattern_ip,re.I)
        m=pattern.match(ip)
        if m:
            return True
        else:
            return False
    def _is_mssql_connect_string(self,dns):
        pattern_mssql_str=r"((?P<servername>\D+\w*)\.db.(?P<env>sh|sh2|sh3|fat|uat|lpt)?(?(env)\.)(?P<domoin>qa.nt.ctripcorp|ctripcorp|ctriptravel){1}\.com,(?P<port>\d+)|(\d{1,3})\.(\d{1,3}).(\d{1,3})\.(\d{1,3}),\d+)"
        pattern=re.compile(pattern_mssql_str,re.I)
        m=pattern.match(dns)
        if m:
            d=m.groupdict()
            return True#,(d["servername"],d["env"],d["domoin"],d["port"])
        else:
            return False#,(None,)
    def _substitute_sql(self,frame):
        cf=self.config_option
        t=SqlTemplate(cf["$sql"])
        return t.substutite(frame.localVariables)

    def run(self,frame):
        sql=self._substitute_sql(frame)
        if '$' not in sql:
            conn=None
            try:
                conn=mssql.get_connect(self.connect_string,self.db)
                if self._hasresult:
                    retset=conn.execute_query_dict(sql)
                    frame.set_local_variable(_result_name,transfer_to_briefobject(retset))
                else:
                    conn.execute_update(sql)
            except Exception, e:
                pass
            finally:
                del conn
        else:
            raise ValueError("sql中有部分变量未替换")

    @property
    def db(self):
        return self.db

    @property
    def connect_string(self):
        return self.connect_string

    @property
    def has_return_set(self):
        return self.has_return_set
    
    def __str__(self):
        return self.substitute_sql(frame)

    def __repr__(self):
        self.__str__

    def serialize_db(self):
        pass




if __name__ == '__main__':

    ss="""
$dns=fltorder.db.ctripcorp.com
$port=55944
$db='fltorderdb'
$sql=
select name 
from $db.sys.tables(nolock)
$return=tablesobject
$a=
select * from sys.databases
$b=

select * from cf_services

"""
    sqlcmd=SqlCommand(ss)
    print sqlcmd.connect_string
