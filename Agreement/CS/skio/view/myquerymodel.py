import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QColor, QBrush

from Agreement.CS.skio.worker.iomapping import get_bit_val
from utils.core import MainWindowConfig


class variableModel(QAbstractTableModel):

    def __init__(self, header, data: list):
        QAbstractTableModel.__init__(self, parent=None)
        self.datas = data
        self.header = header
        self.forceList = set()

    def append_data(self, x):
        self.datas.append(x)
        self.layoutChanged.emit()

    def remove_row(self, row):
        self.datas.pop(row)
        self.layoutChanged.emit()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if len(self.datas) > 0:
            return len(self.datas)
        return 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.header)

    def get_data(self):
        return self

    def data(self, QModelIndex, role=None):
        if role == Qt.BackgroundColorRole:
            if self.datas[QModelIndex.row()][1] in self.forceList:
                return QBrush(QColor(Qt.green))
        if not QModelIndex.isValid():
            print("行或者列有问题")
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()
        if role == Qt.DisplayRole:
            if QModelIndex.column() == 8:
                if self.datas[QModelIndex.row()][7] != None:
                    return QVariant(
                        get_bit_val(MainWindowConfig.IOMapping.current_value[int(self.datas[QModelIndex.row()][5]) - 1][
                                        int(self.datas[QModelIndex.row()][4]) - 1],
                                    int(self.datas[QModelIndex.row()][7])))
                else:
                    return QVariant(MainWindowConfig.IOMapping.current_value[int(self.datas[QModelIndex.row()][5]) - 1][
                                        int(self.datas[QModelIndex.row()][4]) - 1])
            else:
                return QVariant(self.datas[QModelIndex.row()][QModelIndex.column()])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role != Qt.DisplayRole:
            return None


        if orientation == Qt.Horizontal:
            return self.header[section]
