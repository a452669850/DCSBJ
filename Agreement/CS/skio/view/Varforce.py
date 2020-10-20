from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QSplitter, \
    QMessageBox

from utils.WorkModels import PointModel
from utils.core import MainWindowConfig


class varCoercion(QWidget):

    def __init__(self, var, queryModel, row):
        super().__init__()
        self.var = var
        self.queryModel = queryModel
        self.row = row

        self.setWindowTitle('变量强制 %s' % self.var.sig_name)

        self.label = QLabel('设置变量 %s' % self.var.sig_name)
        self.label1 = QLabel('类型 %s' % self.var.sig_type)

        self.line_edit = QLineEdit(self)

        self.btn_OK = QPushButton('OK')
        self.btn_OK.clicked.connect(self.isokbtn)
        self.btn_Cancel = QPushButton('Cancel')
        self.btn_Cancel.clicked.connect(self.close)

        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        layout = QVBoxLayout()

        hbox1.addWidget(QSplitter())
        hbox1.addWidget(self.btn_OK)
        hbox1.addWidget(self.btn_Cancel)
        hbox2.addWidget(self.label)
        hbox2.addWidget(QSplitter())
        hbox3.addWidget(self.label1)
        hbox3.addWidget(QSplitter())

        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.line)
        layout.addLayout(hbox1)
        self.setLayout(layout)

    def getRealAO(self, value, carID, channel):
        i = PointModel.select().where(PointModel.reg == carID, PointModel.channel == channel)[0]
        highValue = i.rhi
        lowValue = i.rlo
        res = 16 * (value - lowValue) / (highValue - lowValue) + 4
        return res / 1000

    def keyPressEvent(self, event):
        # 这里event.key（）显示的是按键的编码
        if str(event.key()) == '16777220':  # 回车
            self.isokbtn()

    # def isokbtn(self):
    #     text = self.line_edit.text()
    #     if self.var.sig_type == 'AO':
    #         try:
    #             var = float(text)
    #         except Exception:
    #             QMessageBox.information(
    #                 self,
    #                 "信息提示",
    #                 "请输入浮点数",
    #                 QMessageBox.Yes | QMessageBox.No
    #             )
    #             return
    #         MainWindowConfig.IOMapping.current_value[int(self.var.reg) - 1][int(self.var.channel) - 1] = self.getRealAO(
    #             var, self.var.reg, self.var.channel)
    #         MainWindowConfig.IOMapping.setAOcurrent()
    #     elif self.var.sig_type == 'PT100':
    #         try:
    #             var = float(text)
    #             var = pt100_t2r(var)
    #         except Exception:
    #             QMessageBox.information(
    #                 self,
    #                 "信息提示",
    #                 "请输入浮点数",
    #                 QMessageBox.Yes | QMessageBox.No
    #             )
    #             return
    #         MainWindowConfig.IOMapping.current_value[int(self.var.reg) - 1][int(self.var.channel) - 1] = var
    #         MainWindowConfig.IOMapping.setAOcurrent()
    #
    #     elif self.var.sig_type == 'TC/T':
    #         try:
    #             var = float(text)
    #             var = RTD_T(var)
    #         except Exception:
    #             QMessageBox.information(
    #                 self,
    #                 "信息提示",
    #                 "请输入浮点数",
    #                 QMessageBox.Yes | QMessageBox.No
    #             )
    #             return
    #         MainWindowConfig.IOMapping.current_value[int(self.var.reg) - 1][int(self.var.channel) - 1] = var
    #         MainWindowConfig.IOMapping.setAOcurrent()
    #
    #     elif self.var.sig_type == 'DO':
    #         try:
    #             if int(text) not in [0, 1]:
    #                 QMessageBox.information(
    #                     self,
    #                     "信息提示",
    #                     "请输入0或1",
    #                     QMessageBox.Yes | QMessageBox.No
    #                 )
    #             val = MainWindowConfig.IOMapping.current_value[int(self.var.reg) - 1][int(self.var.channel) - 1]
    #             MainWindowConfig.IOMapping.current_value[
    #                 int(self.var.reg) - 1][int(self.var.channel) - 1] = set_bit_val(byte=val, val=int(text),
    #                                                                                 index=int(self.var.offset))
    #             MainWindowConfig.IOMapping.setDIcurrent()
    #         except Exception as e:
    #             QMessageBox.information(
    #                 self,
    #                 "信息提示",
    #                 "请输入0或1",
    #                 QMessageBox.Yes | QMessageBox.No
    #             )
    #
    #     else:
    #         return
    #     self.queryModel.forceList.add(self.var.sig_name)
    #     self.queryModel.datas[self.row]['force_value'] = text
    #     self.close()

    def isokbtn(self):
        text = self.line_edit.text()
        if self.var.sig_type in ('AO', 'DO', 'TC/T', 'PT100'):
            self.queryModel.datas[self.row]['force_value'] = text
            MainWindowConfig.IOMapping.force_value[self.var.sig_name] = float(text)
            self.close()
        else:
            QMessageBox.information(
                self,
                "信息提示",
                "该类型无法强制",
                QMessageBox.Yes | QMessageBox.No
            )
