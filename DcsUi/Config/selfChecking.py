from PyQt5.QtCore import QThread, pyqtSignal

from utils import core
from utils.WorkModels import PointModel


class Checking(QThread):
    sinOut = pyqtSignal(list)
    interrupt = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.working = True
        self.num = 0
        self.interrupt.connect(self.forceInterrupt)
        self.data = False

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        points = PointModel.all_points()
        for point in points:
            if self.data:
                break
            try:
                core.MainWindowConfig.IOMapping.read(point.sig_name)
                if point.rlo:
                    core.MainWindowConfig.IOMapping.write(point.sig_name, point.rlo)
                    core.MainWindowConfig.IOMapping.write(point.sig_name, point.rhi)
                    core.MainWindowConfig.IOMapping.write(point.sig_name, (point.rlo + point.rhi) / 2)
                stats = True
                lis = [point.id, point.sig_name, point.sig_type, point.channel, stats]
                self.sinOut.emit(lis)
            except Exception as e:
                stats = False
                lis = [point.id, point.sig_name, point.sig_type, point.channel, stats]
                self.sinOut.emit(lis)

    def forceInterrupt(self):
        self.data = True
