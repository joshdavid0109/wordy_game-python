from Connector import daConnector
import sys
from omniORB import CORBA
import WordyGame

connector = daConnector("localhost", 9999)#should be read sa config
connector.connect()

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
obj = orb.string_to_object("corbaname::localhost:9999")

eo = obj._narrow(WordyGame.WordyGameServer)

def login(self, username, password):
    print(eo.login("ayyyy","ayyyyyo"))