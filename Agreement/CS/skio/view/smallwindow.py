import sys
from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableView, QAbstractItemView, QMenu, QApplication, QHeaderView, QLineEdit, QPushButton, QHBoxLayout, QWidget

from Agreement.CS.skio.view.Varforce import varCoercion
from Agreement.CS.skio.view.myquerymodel import variableModel
from Agreement.CS.skio.worker.iomapping import IOMapping
from utils.WorkModels import PointModel
from utils.core import MainWindowConfig


class tabWidget(QWidget):
    def __init__(self):
        super().__init__()

        # uri = '127.0.0.1:19114'
        # path = Path(__file__).absolute().parent.parent.parent.parent.parent.joinpath('static')
        # imopping = IOMapping(uri=uri, path=path)
        # MainWindowConfig.setIOMapping(imopping)
        # self.path = Path(__file__).absolute().parent.joinpath('static')
        self.searchCon = ''
        self.timer = QTimer()
        self.timer.timeout.connect(self.time)
        self.timer.start(500)
        self.dic = None
        self.getdic()
        hlayout = QHBoxLayout(self)

        layout = QVBoxLayout(self)
        self.lineEdit = QLineEdit(self)
        self.button = QPushButton(self)
        self.button.setText('搜素')
        self.tableView = QTableView(self)
        self.queryModel = variableModel(self.dic['header'], self.dic['data'])
        self.tableView.setModel(self.queryModel)

        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.showContextMenu)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.button.clicked.connect(self.search)

        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.time)

        hlayout.addWidget(self.lineEdit)
        hlayout.addWidget(self.button)
        hlWidget = QWidget()
        hlWidget.setLayout(hlayout)
        layout.addWidget(hlWidget)
        layout.addWidget(self.tableView)

        

        self.setLayout(layout)

    def time(self):
        MainWindowConfig.IOMapping.readall()
        self.update_table()

    def getdic(self):
        self.dic = {
            'header': ['ID', 'SigName', 'type', 'cabinets', 'channel', 'carID', 'size', 'Place number', 'Value', 'minValue', 'maxValue'],
            'data': self.getdicdata()
        }

    def showContextMenu(self):  # 创建右键菜单
        self.tableView.contextMenu = QMenu(self)
        self.actionA = self.tableView.contextMenu.addAction('变量强制')
        self.actionB = self.tableView.contextMenu.addAction('取消强制')
        self.tableView.contextMenu.popup(QCursor.pos())  # 1菜单显示的位置
        self.actionA.triggered.connect(self.actionHandler1)
        self.actionB.triggered.connect(self.actionHandler2)
        self.tableView.contextMenu.show()

    def getdicdata(self):
        lis = []
        self.var_list = PointModel.select()
        for i in self.var_list:
            l = [i.id, i.sig_name, i.sig_type, i.slot, int(i.channel), int(i.reg), i.bit, int(i.offset), '', i.rlo, i.rhi]
            if self.searchCon:
                for x in l:
                    if self.searchCon in str(x):
                        lis.append(l)
                        continue
            else:
                lis.append(l)
        return lis

    def search(self):
        self.searchCon = self.lineEdit.text()
        # self.tableView.claer()
        self.getdic()

    def actionHandler1(self):
        row = self.tableView.currentIndex().row()
        var_name = self.queryModel.datas[row][1]
        var = PointModel.get(PointModel.sig_name == var_name)
        self.var_win = varCoercion(var, self.queryModel)
        self.var_win.show()

    def actionHandler2(self):
        row = self.tableView.currentIndex().row()
        var_name = self.queryModel.datas[row][1]
        var = PointModel.get(PointModel.sig_name == var_name)
        self.var_win = varCoercion(var, self.queryModel)
        self.var_win.line_edit.setText('0')
        self.var_win.isokbtn()
        try:
            self.queryModel.forceList.remove(var_name)
        except:
            pass
        # self.var_win.show()

    def update_table(self):
        self.queryModel.datas = self.getdicdata()
        self.queryModel.layoutChanged.emit()

    def addData(self, lis):
        self.queryModel.append_data(lis)

    def on_timer(self):
        self.queryModel.layoutChanged.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = tabWidget()
    ex.show()
    sys.exit(app.exec_())
