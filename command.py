                                                                 

ss="""

$dns=fltorder.db.ctripcorp.com,55944

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

 

print "-"*30

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

 

class SqlCommand(Command):

    options_fix=["$sql","$dns","$port","$return"]

   

    def __init__(self,str_config):

        self.config_option=parse_param_config(str_config)

        self._check_config(self.config_option)

 

    def _check_config(self):

        cf=self.config

        for option in options_fix:

            try:

                _c=cf[option]

            except KeyError:

                raise ParamError("need this parameter %s" % (option,))

 

 

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