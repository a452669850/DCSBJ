import struct
import sys
from pathlib import Path
import socket

sys.path.append('C:\\Users\\lj\\Desktop\\dcstms-BJDCS-d8e78380ddcb10cf41a485e72e4c2c294ff0122e')
from utils.WorkModels import PointModel, init_database

from peewee import SqliteDatabase
import time

from Agreement.CS.skio.define import AIdataPacket, AOdataPacket, DIdataPacket, HSdataPacket
from Agreement.CS.skio.worker.memory import storeData


class SkIO(object):

    def __init__(self):
        # self.socket = socket.socket()
        self.storeData = storeData()
        # self.set_current_value()

    def setup(self, uri, path):
        # print(uri)
        # host, port = uri.split(':')
        # self._host = host
        # self._port = int(port)
        # self.socket.connect((self._host, self._port))

        for x in ('', 'etc'):
            p = path.joinpath(x)
            if not p.exists():
                p.mkdir(parents=True)

        self.database = SqliteDatabase(path.joinpath('etc', 'skio.db'))
        init_database(self.database)

        self.storeData.setup(path)

    def set_current_value(self):
        self.D_index = set()
        self.AO_index = set()
        self.AI_index = set()
        for i in PointModel.select():
            if i.sig_type in ('DO', 'DI'):
                self.D_index.add(int(i.reg))
                # self.current_value1 = [[0 for w in range(8)] for q in range(len(self.D_index))]
            if i.sig_type == 'AO':
                self.AO_index.add(int(i.reg))
                # self.current_value2 = [[0 for r in range(8)] for e in range(len(self.AO_index))]
            if i.sig_type == 'AI':
                self.AI_index.add(int(i.reg))
                # self.current_value3 = [[0 for y in range(8)] for t in range(len(self.AI_index))]
        # self.current_value = [[0 for x in range(8)] for z in range(len(self.D_index) + len(self.AO_index) + len(self.AI_index))]

    

    def AIread(self, datapack: AIdataPacket):
        # data = []
        t = []
        self.socket.send(datapack.packBytes())
        # 读固定的 12 个字节
        header = self.socket.recv(12)
        start_flag, cmd_type, body_size, pack_no = struct.unpack('>HHLL', header)
        # print(pack_no)
        left_size = body_size
        data = b''
        while left_size:
            buf = self.socket.recv(left_size)
            recv_size = len(buf)
            left_size = left_size - recv_size
            # print('recv {} bytes'.format(recv_size))
            data += buf
        # print(data, 'data1')
        # print(body_size)

        stop_flag = self.socket.recv(2)
        # print('stop_flag: {}'.format(stop_flag))

        frame_size = 8 * 32
        frame_count = int(body_size / frame_size)
        datas = []
        for i in range(frame_count):
            values = struct.unpack('<32d', data[frame_size * i:frame_size * (i + 1)])
            # print(len(values), '2222')
            datas.append(values)
        # print(datas)
        # datas = self.getRealAI(datas)
        # self.set_current_value()
        return datas

    def DIread(self, datapack: AIdataPacket):
        # data = []
        t = []
        self.socket.send(datapack.packBytes())
        # 读固定的 12 个字节
        header = self.socket.recv(12)
        start_flag, cmd_type, body_size, pack_no = struct.unpack('>HHLL', header)
        # print(pack_no)
        left_size = body_size
        data = b''
        while left_size:
            buf = self.socket.recv(left_size)
            recv_size = len(buf)
            left_size = left_size - recv_size
            # print('recv {} bytes'.format(recv_size))
            data += buf
        # print(len(data))
        # print(data)

        stop_flag = self.socket.recv(2)
        # print('stop_flag: {}'.format(stop_flag))

        frame_size = 8 * 8
        frame_count = int(body_size / frame_size)
        datas = []
        for i in range(frame_count):
            values = struct.unpack('<8Q', data[frame_size * i:frame_size * (i + 1)])
            datas.append(values)
        # print(datas, 1111)
        # print(len(datas), 222)
        return datas

    # def DIread(self, datapack: AIdataPacket):
    # data = []
    # t = []
    # self.socket.send(datapack.packBytes())
    # res = self.socket.recv(12)
    # size = int(struct.unpack('>HHLL', res)[2])
    # for i in range(int(size / (6 * 8))):
    # res = self.socket.recv(6 * 8)
    # data1 = struct.unpack('Q' * 6, res)
    # t.append(time.time())
    # data.append(data1)
    # res = self.socket.recv(2)
    # return (data, t)

    def AOwrite(self, datapack: AOdataPacket):
        self.socket.send(datapack.packBytes())
        res = self.socket.recv(14)
        data = struct.unpack('>HHLLH', res)
        return data

    def DIwrite(self, datapack: DIdataPacket):
        self.socket.send(datapack.packBytes())
        res = self.socket.recv(14)
        data = struct.unpack('>HHLLH', res)
        return data

    def start_gather(self, datapack: AIdataPacket):
        self.socket.send(datapack.packBytes())
        res = self.socket.recv(14)
        data = struct.unpack('>HHLLH', res)
        return data

    def stop_gather(self, datapack: AIdataPacket):
        self.socket.send(datapack.packBytes())
        res = self.socket.recv(14)
        data = struct.unpack('>HHLLH', res)
        return data

    def start_high_speed_test(self, datapack: HSdataPacket):
        self.socket.send(datapack.packBytes())
        res = self.socket.recv(14)
        data = struct.unpack('>HHLLH', res)
        return data

    def receive_data(self):
        header = self.socket.recv(12)
        start_flag, cmd_type, body_size, pack_no = struct.unpack('>HHLL', header)
        left_size = body_size
        print(body_size)
        data = b''
        while left_size:
            buf = self.socket.recv(left_size)
            recv_size = len(buf)
            left_size = left_size - recv_size
            # print('recv {} bytes'.format(recv_size))
            data += buf
        # print(data)
        stop_flag = self.socket.recv(2)
        # frame_size = 8 * 16
        # frame_count = int(body_size / frame_size)
        # datas = []
        # for i in range(frame_count):
        # frame_size = 8 * 16
        # frame_count = int(body_size / frame_size)
        # datas = []
        # for i in range(frame_count):
        #     values = struct.unpack('<16d', data[frame_size * i:frame_size * (i + 1)])
        #     datas.append(values)
        values = struct.unpack('<16d', data)
        datas = values
        lis = [0xF312, 18, 0, 0x0000000, 0xF314]
        self.socket.send(struct.pack('>HHLLH', *lis))
        print(datas)
        return datas

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    A = SkIO()
    path = Path(__file__).absolute().parent.joinpath('static')
    A.setup('192.168.10.21:6351', path)

    # print(A.start_gather(B))
    a = 0X000001
    # while True:
    B = DIdataPacket(2, 64, a, [[3, 0, 0, 0], [0, 0, 0, 0]])
    print(A.AIread(B))
    # a += 1
    print(a)
    # time.sleep(0.5)
