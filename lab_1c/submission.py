from asyncio import *
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol


class RequestLogin(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_alex1.MyPacket"
    DEFINITION_VERSION = "2.0"

    FIELDS = [
        ("LoginRequest", STRING)
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
        ("ID", STRING),
        ("PassOrFail", STRING)
    ]


class EchoServerProtocol(Protocol):
    def __init__(self):
        self.transport = None

        self.rl = RequestLogin()
        self.rl.LoginRequest = "Ask for Login"

        self.ii = IdentifyInfo()
        self.ii.pin = 123
        self.ii.IDRequest = "Require ID"
        self.ii.PSWRequest = "Require psw"

        self.ans = Answer()
        self.ans.pin = 123
        self.ans.ID = "Alex"
        self.ans.PSW = "2017alex"

        self.res = Result()
        self.res.ID = 123
        self.res.PassOrFail = ["pass", "fail"]

        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Server Connected to client...")
        self.transport = transport

    def data_received(self, data):
        self.deserializer.update(data)
        for pkt in self.deserializer.nextPackets():
            if pkt == self.rl:
                print("Server: Please provide Login Information")
                self.transport.write(self.ii.__serialize__())
            elif pkt == self.ans:
                print("Server: Login Successfully!")
                self.transport.write(self.res.__serialize__())
            # else: print("Login fails")
        self.transport = None

    def connection_lost(self, exc):
        print("Connection lost!")


class EchoClientProtocol(Protocol):
    def __init__(self):
        self.transport = None

        self.rl = RequestLogin()
        self.rl.LoginRequest = "Ask for Login"

        self.ii = IdentifyInfo()
        self.ii.pin = 123
        self.ii.IDRequest = "Require ID"
        self.ii.PSWRequest = "Require psw"

        self.ans = Answer()
        self.ans.pin = 123
        self.ans.ID = "Alex"
        self.ans.PSW = "2017alex"

        self.res = Result()
        self.res.ID = 123
        self.res.PassOrFail = ["pass", "fail"]

        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Client connects to Server...")
        self.transport = transport
        print("Client: I want to Log in.")
        self.transport.write(self.rl.__serialize__())

    def data_received(self, data):
        self.deserializer.update(data)
        for pkt in self.deserializer.nextPackets():
            if pkt == self.ii:
                print("Client: My id pin is 123, ID is Alex and PSW is 2017alex.")
                self.transport.write(self.ans.__serialize__())
            elif pkt == self.res:
                print("Client: Great")

    def connection_lost(self, exc):
        self.transport = None
        print("The Server stopped and the loop stopped")


def test():
    set_event_loop(TestLoopEx())
    client = EchoClientProtocol()
    server = EchoServerProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)

if __name__ == "__main__":
    test()
