import sys
from omniORB import CORBA
import WordyGame

# APP CONFIG
# Manually pagtype ng method pag first time iinvoke
# -ORBInitRef NameService=corbaname::localhost:9999

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
obj = orb.string_to_object("corbaname::localhost:9999#Hello")  # default corba object name::{host}:{port}

wordyGameServer = obj._narrow(WordyGame.WordyGameServer)

print(wordyGameServer.login("admin", "pass"))

wordyGameServer.playGame();
