import sys
from omniORB import CORBA
from ansys_corba import CosNaming_idl
from configparser import ConfigParser

import WordyGame_idl



orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

ior = sys.argv[1]
obj = orb.string_to_object(ior)

eo = obj._narrow(WordyGame_idl.WordyGameServer)

if eo is None:
    print ("Object reference is not an Example::Echo")
    sys.exit(1)

message = "Hello from Python"
result = eo.logI(message)
