import socket
import struct
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 19114))
sock.listen(10)

while True:
    c, addr = sock.accept()
    while True:
        time.sleep(.1)
        data = c.recv(4)
        if not data:
            break
        a = struct.unpack('>HH', data)[1]
        if a == 1:
            b = c.recv(8)
            # size = struct.unpack('LL', b)[0]
            data = c.recv(512)
            lis1 = [0xF312, 11, 0, 0x0000000, 0xF314]
            c.send(struct.pack('>HHLLH', *lis1))
            print(1)
        if a == 2:
            b = c.recv(8)
            # size = struct.unpack('LL', b)[0]
            data = c.recv(32)
            lis2 = [0xF312, 12, 0, 0x0000000, 0xF314]
            c.send(struct.pack('>HHLLH', *lis2))
            print(2)
        if a == 3:
            b = c.recv(8)
            lis3 = [0xF312, 13, 384, 0x0000000]
            c.send(struct.pack('>HHLL', *lis3))
            lis1 = []
            for i in [[1] * 48]:
                dat = struct.pack('d' * 48, *i)
                c.send(dat)
            c.send(struct.pack('>H', 0xF314))
            print(3)
        if a == 4:
            b = c.recv(8)
            lis4 = [0xF312, 14, 512, 0x0000000]
            c.send(struct.pack('>HHLL', *lis4))
            lis1 = []
            for i in [[1] * 8] * 8:
                dat = struct.pack('Q' * 8, *i)
                c.send(dat)
            c.send(struct.pack('>H', 0xF314))
            print(4)
        if a == 5:
            b = c.recv(8)
            lis5 = [0xF312, 15, 384, 0x0000000, 0xF314]
            c.send(struct.pack('>HHLLH', *lis5))
            print(5)
        if a == 6:
            b = c.recv(8)
            lis6 = [0xF312, 16, 384, 0x0000000, 0xF314]
            c.send(struct.pack('>HHLLH', *lis6))
            print(6)
        if a == 7:
            b = c.recv(8)
            data = c.recv(456)
            lis7 = [0xF312, 17, 0, 0x0000000, 0xF314]
            c.send(struct.pack('>HHLLH', *lis5))
            print(7)
        if a == 8:
            b = c.recv(12)
            print(8)
        c.recv(2)
    #     lis = [0xF312, 14, 192, 0x0000000]
    #     c.send(struct.pack('>HHLL', *lis))
    #     lis1 = []
    #     for i in [[1] * 24]:
    #         dat = struct.pack('d' * 24, *i)
    #         c.send(dat)
    # #     lis1.append(struct.pack('d' * 24, *bytearray(i)))
    # # dat = struct.pack('192s'*8, *lis1)
    # # c.send(dat)
    #     c.send(struct.pack('>H', 0xF314))

# while True:
#     c, addr = sock.accept()
#     data = c.recv(334)
#     print(data)
# lis = [0xF312, 14, 384, 0x0000000]
# c.send(struct.pack('>HHLL', *lis))
# lis1 = []
# for i in [[1] * 6] * 8:
#     dat = struct.pack('Q' * 6, *i)
#     c.send(dat)
# #     lis1.append(struct.pack('Q' * a, *bytearray(i)))
# # dat = struct.pack('192s'*8, *lis1)
# # c.send(dat)
# c.send(struct.pack('>H', 0xF314))


# while True:
#     c, addr = sock.accept()
#     data = c.recv(334)
#     lis = [0xF312, 14, 192, 0x0000000, 0xF314]
#     c.send(struct.pack('>HHLLH', *lis))
