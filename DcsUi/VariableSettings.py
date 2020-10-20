import openpyxl
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from Agreement.CS.skio.model import *
from Agreement.CS.skio.worker.iomapping import pt100_t2r, TC_T, set_bit_val, TC_K, TC_E
from DcsUi.TableFilter import VarDockWidget
from DcsUi.Trend import TrendUi
from DcsUi.VarTreeView import VarTreeDockWidget
from DcsUi.variablecoercion.ToolBarClass import Deploy
# from DcsUi.variablecoercion.displaycolumnWindow import MyWindow
from DcsUi.variablecoercion.ToolBarClassWindow import DeployWindow
from DcsUi.variablecoercion.editTable import configure
from DcsUi.variablecoercion.model import variableGroupModel
from DcsUi.variablecoercion.preservationNewGroup import preservation
from mainwindow import MainWindow
from utils import core
from utils.core import MainWindowConfig


class VariableSettingsUi(MainWindow):
    def __init__(self):
        super(VariableSettingsUi, self).__init__()
        self.group = None
        self.uri = None
        self.initUI()
        self.newInitUI()

    def show(self):
        super(MainWindow, self).show()
        self.dockLeft.setMaximumWidth(300)

    def closeEvent(self, event):
        event.accept()

    def newInitUI(self):
        self.dockTop.deleteLater()
        self.dockLeft.deleteLater()

        self.dockTop = VarDockWidget("变量", self)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockTop)
        self.setCentralWidget(self.dockTop)

        self.dockLeft = VarTreeDockWidget('变量强制窗口', self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockLeft)

        self.splitDockWidget(self.dockLeft, self.dockBottom, Qt.Horizontal)
        self.splitDockWidget(self.dockLeft, self.dockTop, Qt.Horizontal)
        self.splitDockWidget(self.dockTop, self.dockBottom, Qt.Vertical)
        self.setDockNestingEnabled(True)
        self.dockBottom.hide()
        self.dockLeft.setMaximumWidth(250)

    def varforceFindClicked(self):
        self.varforceFindClickedUi = Deploy(group_name=self.group)
        self.varforceFindClickedUi.add_Group_Signal.connect(self.action1)
        self.varforceFindClickedUi.updata_Group_Signal.connect(self.action2)
        self.varforceFindClickedUi.show()

    def varforceEdiTupleClicked(self):
        if self.group == None:
            QMessageBox.information(
                self,
                "信息提示",
                "请选择变量组",
                QMessageBox.Yes | QMessageBox.No
            )
            return
        if not self.dockTop.varTab.currentWidget():
            QMessageBox.information(
                self,
                "信息提示",
                "请选择变量组",
                QMessageBox.Yes | QMessageBox.No
            )
            return
        self.varforceEdiTupleClickedUi = configure(group_name=self.group)
        self.varforceEdiTupleClickedUi.my_Signal.connect(self.action2)
        self.varforceEdiTupleClickedUi.show()

    def varforceNewGroupClicked(self):
        if self.group == None:
            QMessageBox.information(
                self,
                "信息提示",
                "请选择变量组",
                QMessageBox.Yes | QMessageBox.No
            )
            return
        if not self.dockTop.varTab.currentWidget():
            QMessageBox.information(
                self,
                "信息提示",
                "请选择变量组",
                QMessageBox.Yes | QMessageBox.No
            )
            return
        self.varforceNewGroupClickedUi = preservation(group_name=self.group)
        self.varforceNewGroupClickedUi.my_Signal.connect(self.action1)
        self.varforceNewGroupClickedUi.show()

    def varforceAllForceGroupClicked(self):
        self.varforceAllForceGroupClickedUi = DeployWindow(group_name=self.group, win_type=False)
        self.varforceAllForceGroupClickedUi.show()

    def TrendClicked(self):
        self.TrendUi = TrendUi(self.projectPath)
        self.TrendUi.show()

    def varExcelImportClicked(self):
        self.excelPath, filetype = QFileDialog.getOpenFileName(self, '选择文件', '',
                                                               'Excel files(*.xlsx , *.xls)')
        if self.excelPath:
            wb = openpyxl.load_workbook(self.excelPath)
            ws = wb.active
            for row in list(ws.iter_rows())[1:]:
                l = [x.value for x in row]
                try:
                    if not VarModel.get(VarModel.sig_name == row[1].value):
                        VarModel.create(sig_name=row[1].value, type=row[2].value, cabinets=row[3].value,
                                        channel=row[4].value,
                                        carID=row[5].value, PlaceNumber=row[7].value, minValue=row[8].value,
                                        maxValue=row[9].value)
                    else:
                        VarModel.update(type=row[2].value, cabinets=row[3].value, channel=row[4].value,
                                        carID=row[5].value, PlaceNumber=row[7].value, minValue=row[8].value,
                                        maxValue=row[9].value).where(VarModel.sig_name == row[1].value)
                except:
                    VarModel.create(sig_name=row[1].value, type=row[2].value, cabinets=row[3].value,
                                    channel=row[4].value,
                                    carID=row[5].value, PlaceNumber=row[7].value, minValue=row[8].value,
                                    maxValue=row[9].value)
        core.MainWindowConfig.IOMapping.set_current_value()
        self.dockTop.queryModel.datas = self.dockTop.getdicdata()
        self.dockTop.queryModel.layoutChanged.emit()

    def varforceCancelCurrentroupClicked(self):
        '''批量取消强制按钮点击函数'''
        for i in self.dockTop.varTab.currentWidget().queryModel.checkList:
            if i[1] == 'Checked':
                row = i[0]
                MainWindowConfig.IOMapping.write(
                    self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name'],
                    0
                )
                MainWindowConfig.IOMapping.force_value[
                    self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = None
                MainWindowConfig.IOMapping.force_value_stact[
                    self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = False
        QMessageBox.information(
            self,
            "信息提示",
            "取消强制成功",
            QMessageBox.Yes | QMessageBox.No
        )

    def varforceCancelAllforceGroupClicked(self):
        '''批量强制按钮点击函数'''
        for i in self.dockTop.varTab.currentWidget().queryModel.checkList:
            if i[1] == 'Checked':
                row = i[0]
                if self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'] != None:
                    if self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] in ['AO','PT100','TC/K','TC/E','TC/T']:
                        if self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'PT100':
                            try:
                                var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                                var = pt100_t2r(var)
                            except:
                                QMessageBox.information(
                                    self,
                                    "信息提示",
                                    "请输入浮点数",
                                    QMessageBox.Yes | QMessageBox.No
                                )
                                return
                            MainWindowConfig.IOMapping.current_value[
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg'])-1][
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel'])-1
                            ] = var
                            MainWindowConfig.IOMapping.force_value[
                                self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                        elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'TC/T':
                            try:
                                var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                                var = TC_T(var)
                            except:
                                QMessageBox.information(
                                    self,
                                    "信息提示",
                                    "请输入浮点数",
                                    QMessageBox.Yes | QMessageBox.No
                                )
                                return
                            MainWindowConfig.IOMapping.current_value[
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg'])-1][
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel'])-1
                            ] = var
                            MainWindowConfig.IOMapping.force_value[
                                self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                        elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'TC/K':
                            try:
                                var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                                # print(var)
                                var = TC_K(var)
                            except:
                                QMessageBox.information(
                                    self,
                                    "信息提示",
                                    "请输入浮点数",
                                    QMessageBox.Yes | QMessageBox.No
                                )
                                return
                            MainWindowConfig.IOMapping.current_value[
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg'])-1][
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel'])-1
                            ] = var
                            MainWindowConfig.IOMapping.force_value[
                                self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                        elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'TC/E':
                            try:
                                var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                                var = TC_E(var)
                            except:
                                QMessageBox.information(
                                    self,
                                    "信息提示",
                                    "请输入浮点数",
                                    QMessageBox.Yes | QMessageBox.No
                                )
                                return
                            MainWindowConfig.IOMapping.current_value[
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg'])-1][
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel'])-1
                            ] = var
                            MainWindowConfig.IOMapping.force_value[
                                self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                        elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'AO':
                            try:
                                var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                                highValue = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['rhi'])
                                lowValue = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['rlo'])
                                var = getRealAO(var, highValue, lowValue)
                                # print(highValue, lowValue)
                            except:
                                QMessageBox.information(
                                    self,
                                    "信息提示",
                                    "请输入浮点数",
                                    QMessageBox.Yes | QMessageBox.No
                                )
                                return
                            MainWindowConfig.IOMapping.current_value[
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg'])-1][
                                int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel'])-1
                            ] = var
                            # print(MainWindowConfig.IOMapping.current_value)
                            MainWindowConfig.IOMapping.force_value[
                                self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                        MainWindowConfig.IOMapping.setAOcurrent()
                    # elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'PT100':
                    #     try:
                    #         var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                    #         var = pt100_t2r(var)
                    #     except:
                    #         QMessageBox.information(
                    #             self,
                    #             "信息提示",
                    #             "请输入浮点数",
                    #             QMessageBox.Yes | QMessageBox.No
                    #         )
                    #         return
                    #     MainWindowConfig.IOMapping.current_value[
                    #         self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg']][
                    #         self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel']
                    #     ] = var
                    #     MainWindowConfig.IOMapping.force_value[
                    #         self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                    # elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] == 'TC/T':
                    #     try:
                    #         var = float(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                    #         var = RTD_T(var)
                    #     except:
                    #         QMessageBox.information(
                    #             self,
                    #             "信息提示",
                    #             "请输入浮点数",
                    #             QMessageBox.Yes | QMessageBox.No
                    #         )
                    #         return
                    #     MainWindowConfig.IOMapping.current_value[
                    #         self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg']][
                    #         self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel']
                    #     ] = var
                    #     MainWindowConfig.IOMapping.force_value[
                    #         self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = var
                    elif self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_type'] in ('DO-24V', 'DO-48V', 'DO'):
                        # try:
                        # print(int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value']))
                        if int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value']) not in [0,1]:
                            QMessageBox.information(
                                self,
                                "信息提示",
                                "请输入0或1",
                                QMessageBox.Yes | QMessageBox.No
                            )
                        val = MainWindowConfig.IOMapping.current_value[
                            int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg']) - 1][
                            int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['channel']) - 1]
                        MainWindowConfig.IOMapping.current_value[
                            int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['reg']) - 1][
                            int(self.dockTop.varTab.currentWidget().queryModel.datas[row][
                                    'channel']) - 1] = set_bit_val(
                            byte=val,
                            val=int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value']),
                            index=int(self.dockTop.varTab.currentWidget().queryModel.datas[row]['offset'])
                        )
                        MainWindowConfig.IOMapping.force_value[
                            self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = int(
                            self.dockTop.varTab.currentWidget().queryModel.datas[row]['force_value'])
                        MainWindowConfig.IOMapping.setDIcurrent()
                        # except Exception as e:
                        #     print(e)
                        #     QMessageBox.information(
                        #         self,
                        #         "信息提示",
                        #         "请输入0或1",
                        #         QMessageBox.Yes | QMessageBox.No
                        #     )
                else:
                    continue
                MainWindowConfig.IOMapping.force_value_stact[
                    self.dockTop.varTab.currentWidget().queryModel.datas[row]['sig_name']] = True
        # MainWindowConfig.IOMapping.setDIcurrent()
        # MainWindowConfig.IOMapping.setAOcurrent()
        QMessageBox.information(
            self,
            "信息提示",
            "强制值设置成功",
            QMessageBox.Yes | QMessageBox.No
        )

    def action1(self):
        self.dockLeft.refreshTree()

    def action2(self):
        self.dockTop.varTab.currentWidget().queryModel.header = core.MainWindowConfig.header
        self.dockTop.varTab.currentWidget().queryModel.datas = variableGroupModel.selectGroupData(name=self.group)
        self.dockTop.varTab.currentWidget().queryModel.layoutChanged.emit()


def getRealAO(x,highValue, lowValue):
    if highValue:
        return (16 * (x - lowValue) + 4 * (highValue-lowValue))/(1000 * (highValue - lowValue))
    else:
        return x/1000