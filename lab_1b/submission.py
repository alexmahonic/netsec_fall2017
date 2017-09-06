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


def UnitTest1():

    print("This is UnitTest1...")

    packet1 = RequestLogin()
    packet1.LoginRequest = "Ask for Login"
    packet1Bytes = packet1.__serialize__()
    packet1a = RequestLogin.Deserialize(packet1Bytes)
    assert packet1 == packet1a
    if packet1 == packet1a:
        print("packet1 finished: ", packet1.LoginRequest)

    packet2 = IdentifyInfo()
    packet2.pin = 123
    packet2.IDRequest = "Require ID"
    packet2.PSWRequest = "Require psw"
    packet2Bytes = packet2.__serialize__()
    packet2a = IdentifyInfo.Deserialize(packet2Bytes)
    assert packet2 == packet2a
    if packet2 == packet2a:
        print("packet2 finished: ", packet2.pin, ",", packet2.IDRequest, ",", packet2.PSWRequest)

    packet3 = Answer()
    packet3.pin = 123
    packet3.ID = "Alex"
    packet3.PSW = "2017alex"
    packet3Bytes = packet3.__serialize__()
    packet3a = Answer.Deserialize(packet3Bytes)
    assert packet3 == packet3a
    if packet3 == packet3a:
        print("packet3 finished: ", packet3.pin, ",", packet3.ID, ",", packet3.PSW)

    packet4 = Result()
    packet4.ID = "Alex"
    packet4.PassOrFail = "pass"
    packet4Bytes = packet4.__serialize__()
    packet4a = Result.Deserialize(packet4Bytes)
    assert packet4 == packet4a
    if packet4 == packet4a:
        print("packet4 finished: ", packet4.ID, ",", packet4.PassOrFail)

def UnitTest2():

    print("This is UnitTest2...")

    packetAnswer = Answer()
    packetAnswer.pin = 123
    packetAnswer.ID = "Alex"
    packetAnswer.PSW = "2017alex"
    packetAnswerBytes = packetAnswer.__serialize__()

    packetResult = Result()
    packetResult.ID = "Alex"
    packetResult.PassOrFail = "pass"
    packetResultBytes = packetResult.__serialize__()

    TotalBytes = packetAnswerBytes + packetResultBytes

    deserializer = PacketType.Deserializer()
    deserializer.update(TotalBytes)
    for packet in deserializer.nextPackets():
        if packet == packetAnswer: print("Here is packetAnswer")
        elif packet == packetResult: print("Here is pakcetResult")

def UnitTest3():

    print("This is UnitTest3...")

    packetIdenfyInfo = IdentifyInfo()
    try:
        packetIdenfyInfo.pin = -123
    except:
        print("Invalid pin code")

if __name__ == "__main__":
    UnitTest1()
    UnitTest2()
    UnitTest3()
