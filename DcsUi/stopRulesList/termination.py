from PyQt5.QtWidgets import QMessageBox

from DcsUi.stopRulesList.TerminationProcedure import TerminationProcedure
from DcsUi.stopRulesList.stopRulesList import *


class termination(TerminationProcedure):
    def __init__(self, window):
        TerminationProcedure.__init__(self, window)

    def onCombobox1Activate(self):
        conditionChoice = self.all1.currentText()
        text1 = self.qle1.text()
        text2 = self.qle2.text()
        if conditionChoice == "全部":
            conditionChoice = 0
        elif conditionChoice == "规程":
            conditionChoice = 1
        elif conditionChoice == '用例组':
            conditionChoice = 2
        else:
            conditionChoice = 3

        datas = rulesListModel.search_data(type=conditionChoice, number=text1, name=text2)
        self.runList = datas
        self.dic['data'] = datas
        self.queryModel.datas = self.dic['data']

    # 点击查询
    def searchButtonClicked(self):
        self.onCombobox1Activate()
        self.queryModel.layoutChanged.emit()

    def actionHandler1(self):
        self.my_Signal.emit('继续运行')
        self.mainwindow.procedurePauseClicked()

    def actionHandler2(self):
        reply = QMessageBox.information(
            self,
            "信息提示",
            "确认删除该该中止记录吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == 16384:
            row = self.tableView.currentIndex().row()
            RunResult.delete_obj(self.runList[row][5])
            self.runList.pop(row)
            self.queryModel.datas = self.runList
