from asyncio import *
from packet import RequestLogin, Result, Answer, IdentifyInfo
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from playground.network.common import PlaygroundAddress
import playground
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from playground.network.common import StackingProtocolFactory
from playground.network.common import StackingProtocol
from playground.network.common import StackingTransport
import logging

class EchoClientProtocol(Protocol):
    def __init__(self):
        # if callback:
        #     self.callback = callback
        # self.msg = msg
        self.loop = loop
        self.transport = None
        self.rl = RequestLogin()
        self.rl.LoginRequest = True

        # self.ii = IdentifyInfo()
        # self.ii.pin = 123
        # self.ii.IDRequest = "Require ID"
        # self.ii.PSWRequest = "Require psw"

        self.ans = Answer()

        # self.res = Result()
        # self.res.pin = 123
        # self.res.PassOrFail = True

        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Client connects to Server...")
        self.transport = transport
        print("Client: I want to Log in.")
        # self.transport.write(self.rl.__serialize__())

    def data_received(self, data):
        self.deserializer.update(data)
        for pkt in self.deserializer.nextPackets():
            if isinstance(pkt, IdentifyInfo):
                print("Client: Here is my information")
                self.transport.write(self.ans.__serialize__())
            elif isinstance(pkt, Result):
                if pkt.PassOrFail:
                    print("Client: Great!")
                else:
                    print("Client: Oops!")

    def connection_lost(self, exc):
        self.transport = None
        print("The Server stopped and the loop stopped")

    def SendLoginRequest(self):
        self.transport.write(self.rl.__serialize__())

    def SetIdentityInfo(self, pin, ID, PSW):
        self.ans.pin = pin
        self.ans.ID = ID
        self.ans.PSW = PSW


if __name__ == "__main__":
    loop = get_event_loop()
    coro = playground.getConnector().create_playground_connection(lambda: EchoClientProtocol(), '20174.1.1.1', 8888)
    mytransport, myprotocol = loop.run_until_complete(coro)
    myprotocol.SetIdentityInfo(123, "Alex", "2017alex")
    myprotocol.SendLoginRequest()
    logging.getLogger().setLevel(logging.NOTSET)  # this logs *everything*
    logging.getLogger().addHandler(logging.StreamHandler())  # logs to stderr
    loop.run_forever()
    loop.close()
