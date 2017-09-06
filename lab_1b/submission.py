from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER


class RequestLogin(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_alex1.MyPacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("LoginRequest", STRING)
    ]


class IdentifyInfo(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_alex2.MyPacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("pin", UINT32),
        ("IDRequest", STRING),
        ("PSWRequest", STRING)
    ]


class Answer(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_alex3.MyPacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("pin", UINT32),
        ("ID", STRING),
        ("PSW", STRING)
    ]


class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_alex4.MyPacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", STRING),
        ("PassOrFail", STRING)
    ]


def basicUnitTest():
    i = 0

    packet1 = RequestLogin()
    packet1.LoginRequest = "Ask for Login"
    packet1Bytes = packet1.__serialize__()
    packet1a = RequestLogin.Deserialize(packet1Bytes)
    if packet1 == packet1a:
        print("packet1 finished: ", packet1.FIELDS)

    packet2 = IdentifyInfo()
    packet2.pin = 123
    packet2.IDRequest = "Alex"
    packet2.PSWRequest = "2017alex"
    packet2Bytes = packet2.__serialize__()
    packet2a = IdentifyInfo.Deserialize(packet2Bytes)
    if packet2 == packet2a:
        print("packet2 finished: ", packet2.FIELDS)

    packet3 = Answer()
    packet3.pin = 123
    packet3.ID = "Alex"
    packet3.PSW = "2017alex"
    packet3Bytes = packet3.__serialize__()
    packet3a = Answer.Deserialize(packet3Bytes)
    if packet3 == packet3a:
        print("packet3 finished: ", packet3.FIELDS)

    packet4 = Result()
    packet4.ID = "Alex"
    packet4.PassOrFail = "pass"
    packet4Bytes = packet4.__serialize__()
    packet4a = Result.Deserialize(packet4Bytes)
    if packet4 == packet4a:
        print("packet4 finished: ", packet4.FIELDS)

if __name__ == "__main__":
    basicUnitTest()