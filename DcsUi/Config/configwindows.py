import re

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from DcsUi.Config.configure import textEnvironment, networkConfiguration, environmentChecking, timeInterval
from DcsUi.Config.getData import getListData
from DcsUi.Config.importThread import myQThreading
from DcsUi.userManagement.AccountManagement import AccountManagement
from utils import core
from utils.WorkModels import *


class textEnviron(textEnvironment):
    def __init__(self):
        textEnvironment.__init__(self)

    def leadingIn(self):
        dirPath = QtWidgets.QFileDialog.getOpenFileName(self,
                                                        "选取文件",
                                                        "./"
                                                        )[0]
        if dirPath != '':
            self.threading = myQThreading(path=dirPath)
            self.threading.sinOut.connect(self.textset)
            self.threading.start()

    def getdicdata(self):
        lis = []
        dev_list = NetworkConfig.filter(NetworkConfig.protocol == 'TCP/IP')
        var_list = PointModel.filter(PointModel.slot.in_([x.slot for x in dev_list])).order_by(PointModel.id)
        for i in var_list:
            self.list_name.append(i)
            lis.append([i.id, i.sig_name, i.sig_type, i.slot, i.channel])
        return lis

    def textset(self, text):
        if text == '导入Excel完成\n':
            self.queryModel.datas = self.getdicdata()
            self.queryModel.layoutChanged.emit()

    def search(self):
        lis = []
        text = self.line.text()
        for i in self.list_name:
            if text in i.sig_name:
                lis.append([i.id, i.sig_name, i.sig_type, i.slot, i.channel])
        self.queryModel.datas = lis
        self.queryModel.layoutChanged.emit()


class networkConfig(networkConfiguration):
    def __init__(self):
        networkConfiguration.__init__(self)

    def getdicdata(self):
        lis = []
        datas = NetworkConfig.select()
        for x in datas:
            lis.append([x.id, x.slot, x.description, x.uri])
        return lis

    def search(self):
        text = self.line.text()
        datas = getListData.search_NetworkConfig(text)
        self.queryModel.datas = datas
        self.queryModel.layoutChanged.emit()


class environmentCheck(environmentChecking):
    def __init__(self):
        environmentChecking.__init__(self)

    def startSelfscan(self):
        if self.threading.isRunning():
            QMessageBox.information(
                self,
                "信息提示",
                "正在自检请勿点击",
                QMessageBox.Yes | QMessageBox.No
            )
            return
        else:
            self.queryModel.datas = []
            self.queryModel.layoutChanged.emit()
            self.threading.start()

    def slotAdd(self, lis):
        self.queryModel.append_data(lis)


class timeInter(timeInterval):
    def __init__(self):
        timeInterval.__init__(self)

    def confirm(self):
        fieldData = {}
        qletext = self.qle.text()
        boxtext = self.box.currentText()
        fieldData['time'] = qletext or str((core.MainWindowConfig.RunInterval or 0.5) * 1000)
        fieldData['ensure'] = boxtext or core.MainWindowConfig.ContinueRunFalse
        continue_run_false = True if fieldData['ensure'] == u'是' else False
        if re.match(r'^[0-9]+\.[0-9]+$', fieldData['time']):
            if int(float(fieldData['time'])) > 3000 or int(float(fieldData['time'])) < 300:
                QMessageBox.information(
                    self,
                    "信息提示",
                    "请输入300-3000之间的整数！",
                    QMessageBox.Yes | QMessageBox.No
                )
            else:
                set_time = float(fieldData['time'])
                core.MainWindowConfig.ContinueRunFalse = continue_run_false
                core.MainWindowConfig.RunInterval = set_time
                QMessageBox.information(
                    self,
                    "信息提示",
                    "设置成功，请关闭窗口！",
                    QMessageBox.Yes | QMessageBox.No
                )
        else:
            QMessageBox.information(
                self,
                "信息提示",
                "输入有误，请重新输入！",
                QMessageBox.Yes | QMessageBox.No
            )


class configureWindow(AccountManagement):
    def __init__(self):
        super().__init__()
        self.setObjectName('配置')
        self.setWindowTitle('配置')

    def _setdata_(self):
        win1 = textEnviron()
        win2 = networkConfig()
        win3 = environmentCheck()
        # win4 = timeInter()
        self.lis_name = ['测试环境', '网络配置', '环境自检']
        self.lis_win = [win1, win2, win3]
        self.lis_img = [
            ':/static/environment_settings_icon0.png',
            ':/static/NetworkSettings.png',
            ':/static/VariableSettings.png',
            # ':/static/time_interval.png'
        ]

    def changeData(self):
        win = self.right_widget.currentWidget()
        if hasattr(win, 'getdicdata'):
            win.queryModel.datas = win.getdicdata()
            win.queryModel.layoutChanged.emit()

    def closeEvent(self, event):
        win = self.right_widget.widget(2)
        win.threading.interrupt.emit('')
        self.close()
