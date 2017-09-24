from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from playground.network.common import *
import playground


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