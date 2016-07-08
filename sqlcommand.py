import re
import os
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


print parse_param_config(ss)


class ParamError(Exception):
    def __init__(self,msg):
        super(ParamError,self).__init__(msg)




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



class SqlCommand(Command):
    """
    $sql 必填参数，可执行的sql语句
    $dns 可选参数，只执行sql的目标服务器，该变量可继承
    $port 可选参数，当$dns是域名或者IP时，那么一定要提供$port
    $return 可选参数，临时存储查询结果集时，指定结果集的名称

    example:
        $sql=select name,object_id 
        from sys.databases(nolock)
        $dns=fltorder.db.ctripcorp.com,55944
        $return=tableinfo
    """
    options_fix=["$sql","$dns"]
    options_option=["$return"]
    
    def __init__(self,str_config):
        self.config_option=parse_param_config(str_config)
        self._check_config(self.config_option)

    def _check_config(self):
        cf=self.config
        for option in options_fix:
            try:
                _ov=cf[option]
                if option=="$dns":
                    is_mssql,data= self._is_mssql_connect_string(_ov)
                    if not is_mssql:
                        if not cf.has_key("$port"):
                            raise ParamError("lack the parameter $port")
                    else self._is_dns(_ov) or self._is_ip(_ov):
                        if "$port" not in cf :
                    else:
                        raise ParamError("need this parameter %s" % (option,))
            except KeyError:
                raise ParamError("need this parameter %s" % (option,))

    def _is_dns(self):
        pattern_dns=r"(?P<servername>\D+\w*)\.db.(?P<env>sh|sh2|sh3|fat|uat|lpt)?(?(env)\.)(?P<domoin>qa.nt.ctripcorp|ctripcorp|ctriptravel){1}\.com,(?P<port>\d+)"
        pattern=re.compile(pattern_dns,re.I)
        m=pattern.match(dns)
        if m:
            return True
        else:
            return False
    def _is_ip(self):
        pattern_ip=r"(\d{1,3})\.(\d{1,3}).(\d{1,3})\.(\d{1,3})"
        pattern=re.compile(pattern_ip,re.I)
        m=pattern.match(dns)
        if m:
            return True
        else:
            return False
    def _is_mssql_connect_string(self):
        pattern_mssql_str=r"(?P<servername>\D+\w*)\.db.(?P<env>sh|sh2|sh3|fat|uat|lpt)?(?(env)\.)(?P<domoin>qa.nt.ctripcorp|ctripcorp|ctriptravel){1}\.com,(?P<port>\d+)"
        pattern=re.compile(pattern_mssql_str,re.I)
        m=pattern.match(dns)
        if m:
            d=m.groupdict()
            return True,(d["servername"],d["env"],d["domoin"],d["port"])
        else:
            return False,(None,)
    def substitute_sql(self,frame):
        t=SqlTemplate(self._sql)
        return t.substutite(frame.localVariables)
    def run(self,frame):
        sql=self.substitute_sql(frame)
        if '$' not in sql:
            conn=None
            try:
                conn=mssql.get_connect(self._host,self._db)
                if self._hasresult:
                    retset=conn.execute_query_dict(substitute_sql(self._sql))
                    frame.set_local_variable(_result_name,transfer_to_briefobject(retset))
                else:
                    conn.execute_update(sql)
            except Exception, e:
                pass
            finally:
                del conn
        else:
            raise ValueError("sql中有部分变量未替换")

    def __str__(self):
        return self.substitute_sql(frame)

    def __repr__(self):
        self.__str__

    def serialize_db(self):
        pass