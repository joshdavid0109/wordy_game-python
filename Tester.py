import sys
from omniORB import CORBA

from ClientApp import Connector

con = Connector(sys.argv)

con.hello.sayHello()