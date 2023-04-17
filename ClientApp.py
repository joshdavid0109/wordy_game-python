#!/usr/bin/env python

import sys

from omniORB import CORBA
from COS import CosNaming_idl
from configparser import ConfigParser

class Connector:

    def __init__(self, args):
        self.read_config()
        # initialise orb object
        if len(args) > 1:
            self.orb = CORBA.ORB_init(args, CORBA.ORB_ID)
        elif len(self.args) > 1:
            self.orb = CORBA.ORB_init(self.args, CORBA.ORB_ID)

        self.obj = self.orb.resolve_initial_references("NameService")
        self.rootContext = self.obj._narrow(CosNaming_idl.NamingContext)

        if self.rootContext is None:
            print("Failed to narrow the root naming context")
            sys.exit(1)

        self.name = [CosNaming_idl.NameComponent('Hello', '')]

        try:
            self.obj = self.rootContext.resolve(self.name)
        except CosNaming_idl.NamingContext.NotFound as ex:
            print("name not found")
            sys.exit(1)

        self.hello = self.obj._narrow(HelloApp.Hello)

        print("gumagana")


    def read_config(self):
        self.args = []

        # read the configuration file
        # config = ConfigParser()
        # config.read('config.ini')

        host = "localhost"
        port = 900

        self.args = ['connector.py', '-ORBInitRef', 'NameService=corbaname::{host}:{port}'.format(host=host, port=port)]

    # self.helloApp = self.obj._narrow(HelloApp.HelloApp_idl.Hello)

    # self.helloApp.sayHello();

# orb = CORBA.ORB_init(sys.argv, )
# poa = orb.resolve_initial_references("RootPOA")
#
# poaManager = poa._get_the_POAManager()
# poaManager.activate()
# print("Server is ready to accept clients")
#
# # message = "Hello"
# # result = eo.echoString(message)
# #
# # print("I said '%s'. The object said '%s'." % (message, result))
#
#
# orb.run()
