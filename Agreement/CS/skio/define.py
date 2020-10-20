import struct


# from skio.worker.state import SlotInfo


class DIdataPacket(object):

    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int, lis: list):
        self.data_type = data_type
        self.data_size = data_size
        self.Packet_serial_No = Packet_serial_No

        lis1 = []
        for i in lis:
            lis1 += i
        # print(lis1)

        self.value = struct.pack('8Q', *lis1)
        # print(len(self.value))
        self.array = []

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, self.value, 0xF314
        ]
        # print(self.buf)
    def packBytes(self):
        packstyle = '>HHLL64sH'
        req = struct.pack(packstyle, *self.buf)
        return req


class AOdataPacket(object):
    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int, lis: list):
        self.data_type = data_type
        self.data_size = data_size
        self.Packet_serial_No = Packet_serial_No
        self.value = struct.pack('d' * 80, *lis)

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, self.value, 0xF314
        ]
        # print(self.buf)
    def packBytes(self):
        packstyle = '>HHLL640sH'
        req = struct.pack(packstyle, *self.buf)
        return req


class AIdataPacket(object):
    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int):
        self.data_type = data_type
        self.data_size = data_size
        self.Packet_serial_No = Packet_serial_No

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, 0xF314
        ]

    def packBytes(self):
        packstyle = '>HHLLH'
        req = struct.pack(packstyle, *self.buf)
        return req


class GSstartdataPacket(object):
    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int):
        self.data_type = data_type
        self.data_size = data_size
        self.Packet_serial_No = Packet_serial_No

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, 0xF314
        ]

    def packBytes(self):
        packstyle = '>HHLLH'
        req = struct.pack(packstyle, *self.buf)
        return req


class GSstopdataPacket(object):
    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int):
        self.data_type = data_type
        self.data_size = data_size
        self.Packet_serial_No = Packet_serial_No

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, 0xF314
        ]

    def packBytes(self):
        packstyle = '>HHLLH'
        req = struct.pack(packstyle, *self.buf)
        return req


class HSdataPacket(object):
    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int, lis: list):
        self.data_type = data_type
        self.data_size = 456
        self.Packet_serial_No = Packet_serial_No
        self.value = struct.pack('d' * 57, *lis)
        print(self.data_type,self.data_size)

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, self.value, 0xF314
        ]

    def packBytes(self):
        packstyle = '>HHLL456sH'
        req = struct.pack(packstyle, *self.buf)
        return req


class STDdataPacket(object):
    def __init__(self, data_type: int, data_size: int, Packet_serial_No: int, lis: list):
        self.data_type = data_type
        self.data_size = data_size
        self.Packet_serial_No = Packet_serial_No
        self.value = struct.pack('d' * self.data_size / 8, *lis)

        self.buf = [
            0xF312, self.data_type, self.data_size, self.Packet_serial_No, self.value, 0xF314
        ]

    def packBytes(self):
        packstyle = '>HHLL%ssH' % self.data_size
        req = struct.pack(packstyle, *self.buf)
        return req


if __name__ == '__main__':
    A = AOdataPacket(1, 320, 0X0000000, [1] + [0] * 39)
    print(A.value)
    A.packBytes()
    print(A.packBytes())
