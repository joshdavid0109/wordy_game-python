import sys
from omniORB import CORBA
import WordyGame

# APP CONFIG
# -ORBInitRef NameService=corbaname::localhost:9999

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
obj = orb.string_to_object("corbaname::localhost:9999#Hello")  # default corba object name::{host}:{port}

eo = obj._narrow(WordyGame.WordyGameServer)

print(eo.login("admin", "pass"))
