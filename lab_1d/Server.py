from asyncio import *
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
import playground
from playground.network.common import PlaygroundAddress
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol


class RequestLogin(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_a1.MyPacket"
    DEFINITION_VERSION = "3.0"

    FIELDS = [
        ("LoginRequest", BOOL)
    ]


class IdentifyInfo(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_a2.MyPacket"
    DEFINITION_VERSION = "3.0"

    FIELDS = [
        ("pin", UINT32),
        ("IDRequest", STRING),
        ("PSWRequest", STRING)
    ]


class Answer(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_a3.MyPacket"
    DEFINITION_VERSION = "3.0"

    FIELDS = [
        ("pin", UINT32),
        ("ID", STRING),
        ("PSW", STRING)
    ]


class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab1c.student_a4.MyPacket"
    DEFINITION_VERSION = "3.0"

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
        # print("Server Connected to client...")
        peername = transport.get_extra_info("peername")
        print('Connection from {}'.format(peername))
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

if __name__ == "__main__":
    loop = get_event_loop()
    # coro = loop.create_server(lambda:EchoServerProtocol(),'127.0.0.1', 8000)
    coro = playground.getConnector().create_playground_server(lambda : EchoServerProtocol(), '20174.1.1.1', 58300)
    myserver = loop.run_until_complete(coro)
    loop.run_forever()
    myserver.close()
    loop.close()
