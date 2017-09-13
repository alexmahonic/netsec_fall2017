from asyncio import *
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol


class RequestLogin(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_alex1.MyPacket"
    DEFINITION_VERSION = "2.0"

    FIELDS = [
        ("LoginRequest", BOOL)
    ]


class IdentifyInfo(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_alex2.MyPacket"
    DEFINITION_VERSION = "2.0"

    FIELDS = [
        ("pin", UINT32),
        ("IDRequest", STRING),
        ("PSWRequest", STRING)
    ]


class Answer(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_alex3.MyPacket"
    DEFINITION_VERSION = "2.0"

    FIELDS = [
        ("pin", UINT32),
        ("ID", STRING),
        ("PSW", STRING)
    ]


class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_alex4.MyPacket"
    DEFINITION_VERSION = "2.0"

    FIELDS = [
        ("pin", STRING),
        ("PassOrFail", BOOL)
    ]


class EchoServerProtocol(Protocol):
    def __init__(self):
        self.transport = None

        # self.rl = RequestLogin()
        # self.rl.LoginRequest = True

        self.ii = IdentifyInfo()
        self.ii.pin = 123
        self.ii.IDRequest = "Require ID"
        self.ii.PSWRequest = "Require psw"

        self.ans = Answer()
        self.ans.pin = 123
        self.ans.ID = "Alex"
        self.ans.PSW = "2017alex"

        self.res = Result()
        self.res.pin = 123
        # self.res.PassOrFail = True

        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Server Connected to client...")
        self.transport = transport

    def data_received(self, data):
        self.deserializer.update(data)
        for pkt in self.deserializer.nextPackets():
            if isinstance(pkt, RequestLogin):
                print("Server: Please provide Login Information")
                self.transport.write(self.ii.__serialize__())
            elif isinstance(pkt, Answer):
                if pkt.pin == self.ans.pin and pkt.ID == self.ans.ID and pkt.PSW == self.ans.PSW:
                    print("Server: Login Successfully!")
                    self.res.PassOrFail = True
                    self.transport.write(self.res.__serialize__())
                else:
                    print("Server: Authentication denied!")
                    self.res.PassOrFail = False
                    self.transport.write(self.res.__serialize__())
                    # else: print("Login fails")
        # self.transport = None

    def connection_lost(self, exc):
        print("Connection lost!")


class EchoClientProtocol(Protocol):
    def __init__(self, callback = None):
        if callback:
            self.callback = callback

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


def UnitTest1():
    clientProtocol = EchoClientProtocol()
    serverProtocol = EchoServerProtocol()
    transportToServer = MockTransportToProtocol(myProtocol=clientProtocol)
    transportToClient = MockTransportToProtocol(myProtocol=serverProtocol)
    transportToServer.setRemoteTransport(transportToClient)
    transportToClient.setRemoteTransport(transportToServer)
    clientProtocol.connection_made(transportToServer)
    serverProtocol.connection_made(transportToClient)

    clientProtocol.SetIdentityInfo(123, "Alex", "2017alex")
    clientProtocol.SendLoginRequest()


def UnitTest2():
    clientProtocol = EchoClientProtocol()
    serverProtocol = EchoServerProtocol()
    cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(clientProtocol, serverProtocol)
    clientProtocol.connection_made(cTransport)
    serverProtocol.connection_made(sTransport)

    clientProtocol.SetIdentityInfo(123, "Jack", "2017jack")
    clientProtocol.SendLoginRequest()

if __name__ == "__main__":
    UnitTest1()
    print("--------------------")
    UnitTest2()
