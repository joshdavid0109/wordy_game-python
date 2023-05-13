import sys
from omniORB import CORBA

from Connector import Connector

con = Connector(sys.argv)

con.hello.sayHello()