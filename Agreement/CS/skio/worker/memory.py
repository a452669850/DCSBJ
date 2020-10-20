import datetime
import os
import struct
import threading
from pathlib import Path


class storeData(object):

    def __init__(self):
        self.path = None
        self.fd = None
        self.lock = threading.RLock()

    def setup(self, path):
        with self.lock:
            self.path = path
            self.__create__data()

    def __create__data(self):
        st = str(datetime.datetime.now().date()) + '.dat'
        self.fd = os.open(
            self.path.joinpath(st).as_posix(),
            flags=os.O_CREAT | os.O_RDWR | os.O_APPEND
        )

    def write(self, time, datapacket):
        os.write(self.fd, struct.pack('d', time))
        os.write(self.fd, b'\n')
        os.write(self.fd, datapacket)
        os.write(self.fd, b'\n')


if __name__ == '__main__':
    lis = []
    a = None
    for i in [[1, ] * 8, [2] * 8, [3] * 8, [4] * 8]:
        a = len(bytearray(i))
        lis.append(struct.pack('%ds' % a, bytearray(i)))
    data = struct.pack('%ds' % a * len(lis), *lis)
    a = storeData()
    path = Path(__file__).absolute().parent.parent.joinpath('static')
    a.setup(path)
