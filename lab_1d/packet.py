from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
import playground

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