# Tester class

import sys
from omniORB import CORBA
import WordyGame

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
obj = orb.string_to_object("corbaname::localhost:9999")

eo = obj._narrow(WordyGame.WordyGameServer)

print(eo.login("admin", "pass"))
