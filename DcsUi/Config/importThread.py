import re

import xlrd
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

from DcsUi.Config.getData import getListData
from utils.WorkModels import NetworkConfig, PointModel
from utils.core import MainWindowConfig

qmut = QMutex()


class myQThreading(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, path):
        super().__init__()
        self.working = True
        self.path = path

    def __del__(self):
        self.working = False
        self.wait()

    def run(self) -> None:
        qmut.lock()
        name = self.path.replace(re.search('.*/', self.path).group(), '')
        self.sinOut.emit('正在解析Excel：%s\n' % name)
        workbook = xlrd.open_workbook(self.path)
        network_table = workbook.sheet_by_name('SLOT')
        ni_pxi_table = workbook.sheet_by_name('PXI')

        self.load_dev_table(network_table)
        self.load_var_table(ni_pxi_table)

        self.sinOut.emit('导入Excel完成\n')
        MainWindowConfig.IOMapping.setupvalue()
        getListData.create_group('allVariables')

        self.exec_()
        qmut.unlock()

    def load_dev_table(self, sheet):
        bulk = []
        dic = {
            'slot': 'slot',
            'protocol': 'protocol',
            'ip': 'ip',
            'port': 'port',
            'desc': 'description'
        }
        for rowx in range(1, sheet.nrows):
            row_data = sheet.row_values(rowx)
            item_dict = {}
            for index, key in enumerate(sheet.row_values(0)):
                if key not in dic:
                    continue
                if key == 'ip':
                    self.ip = row_data[index]
                    continue
                if key == 'port':
                    self.port = row_data[index]
                    continue
                item_dict[dic[key]] = row_data[index]
            item_dict['uri'] = self.ip + ':' + str(int(self.port))
            bulk.append(item_dict)

        self.sinOut.emit('正在清空设备表\n')
        NetworkConfig.delete().execute()
        self.sinOut.emit('正在插入设备表\n')
        NetworkConfig.insert_many(bulk).execute()
        self.sinOut.emit('导入设备表完成\n')

    def load_var_table(self, sheet):
        bulk = []
        for rowx in range(1, sheet.nrows):
            row_data = sheet.row_values(rowx)
            item_dict = {}
            for index, key in enumerate(sheet.row_values(0)):
                if key in ('rlo', 'rhi', 'elo', 'ehi', 'offset'):
                    value = row_data[index]
                    try:
                        value = float(value)
                    except (TypeError, ValueError):
                        value = None
                    item_dict[key] = value
                    continue
                else:
                    item_dict[key] = row_data[index]
            bulk.append(item_dict)
        self.sinOut.emit('正在清空变量表\n')
        PointModel.delete().execute()
        chunk = []
        for x in bulk:
            chunk.append(x)
            if len(chunk) < 50:
                continue
            self.sinOut.emit('正在插入变量表\n')
            PointModel.insert_many(chunk).execute()
            chunk.clear()
        self.sinOut.emit('正在插入变量表\n')
        PointModel.insert_many(chunk).execute()
        chunk.clear()
        bulk.clear()
        self.sinOut.emit('导入变量表完成\n')
