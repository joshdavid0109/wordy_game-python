import sys
import traceback

from omniORB import CORBA
import WordyGame

# APP CONFIG
# Manually pagtype ng method pag first time iinvoke
# -ORBInitRef NameService=corbaname::localhost:9999

eo = None

class daConnector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.orb = None
        self.wordyGameServer = None

    def connect(self):
        try:
            self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
            obj = self.orb.string_to_object(f"corbaname::{self.host}:{self.port}#Hello")
            self.wordyGameServer = obj._narrow(WordyGame.WordyGameServer)
            global eo
            eo = obj._narrow(WordyGame.WordyGameServer)
            print("CONNECTED:)\n\n")
        except Exception as e:
            traceback.print_exc()
            print(e)
