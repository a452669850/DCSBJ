# -*- coding:utf-8 -*-
import sys
import socket
import json
import time
import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QApplication, QWidget, QAction, QMenu, \
    QSystemTrayIcon

from DcsUi.Config.configwindows import configureWindow
from DcsUi.ExcelDockWidget import TabDockWidget
from DcsUi.LogDockWidget import LogDockWidget
from DcsUi.LogWindow import LogWindow
from DcsUi.MainToolBarClass import ToolBarSetting
from DcsUi.TreeView import TreeDockWidget
from DcsUi.pharse import PhraseUI
from DcsUi.proceduresManage import proceduresWindow
from DcsUi.stopRulesList.termination import termination
from DcsUi.testRecord.textRecordWindow import textRecordWindow
from DcsUi.useCaseGroupManagement.proceduresManage import proceduresWindow
from DcsUi.userManagement.accountManage import AccountManage
from procedure.manage_procedure.import_procedure import parse_procedure
from procedure.run_procedure.RunProceduree import ProcedureThread
from tools.JsonConfig import getProjectName, writeJson
from utils.InitDb import connectDb, judgeProjectPath
from utils.core import MainWindowConfig
from utils.WorkModels import NetworkConfig


# from procedure.run_procedure.runconfig import RunConfig
# from communication.communicationWindow import comWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.projectPath = None
        self.projectName = None
        self.procedureRunIndex = 0
        self.procedureRunPath = None

    def initUI(self):
        self.projectName = getProjectName(self.projectPath)

        # 连接数据库
        self.dbPath = connectDb(self.projectPath)

        # 建立tcp连接
        if self.__class__.__name__ == 'MainWindow':
            self.getUrl()
            self.socket = socket.socket()
            MainWindowConfig.IOMapping.skio.socket = self.socket
            self.timer = QTimer(self) #初始化一个定时器
            self.timer.timeout.connect(self.connect) #计时结束调用connect()方法
            self.timer.start(3000) #设置计时间隔并启动

        # 创建工具栏和菜单栏
        self.toolBarSetting = ToolBarSetting(self)
        # 创建一个状态栏
        self.statusBar = self.statusBar()

        # 初始化dock控件
        self.dockTop = TabDockWidget("Console", self)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockTop)
        self.setCentralWidget(self.dockTop)
        # log标签dock
        self.dockBottom = LogDockWidget("Log", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockBottom)
        # tree结构dock
        self.dockLeft = TreeDockWidget("Project Explorer", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockLeft)

        # 设置初始dock大小
        self.dockLeft.setMaximumWidth(100)  # 设置最大宽度
        self.dockBottom.setMaximumHeight(250)  # 设置最大高度

        # 设置Dock布局
        self.splitDockWidget(self.dockLeft, self.dockBottom, Qt.Horizontal)
        self.splitDockWidget(self.dockLeft, self.dockTop, Qt.Horizontal)
        self.splitDockWidget(self.dockTop, self.dockBottom, Qt.Vertical)
        self.setDockNestingEnabled(True)  # 开启dock嵌套

        # 初始化窗体
        self.setWindowIcon(QIcon(':/static/default.png'))
        self.setWindowTitle(f"Dcs自动化测试软件[{self.projectName}]")
        self.setWindowState(Qt.WindowMaximized)
        self.addSystemTray()
        QApplication.setStyle('Fusion')

        #  初始化规程线程
        self.ProcedureThread = ProcedureThread(parent=self)

        self.log = LogWindow(self)

    def getUrl(self):
        try:
            self.url = NetworkConfig.select()[0].uri
            host, port = self.url.split(':')
            self.url = (host, int(port))
        except:
            self.url = None

    def connect(self):
        if self.url:
            try:
                self.socket.connect(self.url)
                MainWindowConfig.IOMapping.STOP_GS_experiment()
                # print(3)
                time.sleep(1)
                # print(1)
                MainWindowConfig.IOMapping.stop_gather()
                time.sleep(1)
                # print(2)
                MainWindowConfig.IOMapping.start_gather(self)
                self.statusBar.showMessage('已连接')
            except Exception as e:
                if type(e) == ConnectionRefusedError:
                    self.statusBar.showMessage('未连接')
                else:
                    # print(e)
                    pass
        else:
            self.statusBar.showMessage('未配置网络')
            self.getUrl()

    def show(self):
        super(MainWindow, self).show()
        self.dockLeft.setMaximumWidth(1920)

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     'Quit',
                                     "是否要退出程序？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            MainWindowConfig.IOMapping.stop_gather()
            try:
                MainWindowConfig.IOMapping.skio.close()
            except Exception as e:
                print(e)
            writeJson(self.projectPath)
            event.accept()
        else:
            event.ignore()

    def viewDefaultClicked(self):
        QApplication.processEvents()

    def projectCreateClicked(self):
        # 创建工程
        from DcsUi.newbuild import Ui_NewBuild
        self.projectCreateUi = Ui_NewBuild(parent=self)
        self.projectCreateUi.mainIsWorking = True
        self.projectCreateUi.show()

    def projectOpenClicked(self):
        # 打开工程
        self.newProjectPath = QFileDialog.getExistingDirectory(self, '选择文件夹', './')
        if judgeProjectPath(self.newProjectPath) and self.newProjectPath != self.projectPath:
            self.projectPath = self.newProjectPath
            connectDb(self.projectPath)
            self.projectName = getProjectName(self.projectPath)
            self.dockTop.setWidget(QWidget())
            self.dockLeft.refreshTree()
            self.dockBottom.logBrowser.clear()
            self.log.infoLog(f'切换工程至:{self.projectName}')

    def projectSaveClicked(self):
        print('pk')

    def proceduresImportClicked(self):
        # 导入规程
        self.procedurePathList, filetype = QFileDialog.getOpenFileNames(self, '选择文件', '',
                                                                   )  # 设置文件扩展名过滤,注意用双分号间隔
        if len(self.procedurePathList) == 2:
            for x in self.procedurePathList:
                # print(x.split('.')[-1])
                if x.split('.')[-1] == 'docx' or x.split('.')[-1] == 'doc':
                    wordPath = x
                elif x.split('.')[-1] == 'xlsx' or x.split('.')[-1] == 'xls':
                    excelPath = x
                    # print(excelPath)
            if excelPath:
                proName = parse_procedure(excelPath, wordPath)
                a = self.dockLeft.insertProToJson(self.dockLeft.treeDict, proName)
                print(a)
                proJsonPath = os.path.join(self.projectPath, '.userdata', 'Pro.json')
                with open(proJsonPath, 'w', encoding='utf-8') as f:
                    json.dump(a, f)
                self.dockLeft.refreshTree()
                self.log.infoLog(f'成功导入{excelPath}')
        elif len(self.procedurePathList) == 1:
            if self.procedurePathList[0]:
                proName = parse_procedure(self.procedurePathList[0])
                a = self.dockLeft.insertProToJson(self.dockLeft.treeDict, proName)
                print(a)
                proJsonPath = os.path.join(self.projectPath, '.userdata', 'Pro.json')
                # with open(proJsonPath, 'w', encoding='utf-8') as f:
                #     json.dump(a, f)
                self.dockLeft.refreshTree()
                self.log.infoLog(f'成功导入{self.procedurePathList[0]}')

    # def proceduresExportClicked(self):
    #     print(self)

    def varforceUpdateGroupClicked(self):
        # 用例组管理
        self.varforceUpdateGroupUi = proceduresWindow()
        self.varforceUpdateGroupUi.proced_Signal.connect(self.active_update)
        self.varforceUpdateGroupUi.setWindowModality(Qt.ApplicationModal)
        self.varforceUpdateGroupUi.show()

    # def proceduresDeleteClicked(self):
    #     # 删除规程
    #     print(self)

    def proceduresSettingsClicked(self):
        # 规程配置按钮
        self.proceduresSettingsUi = configureWindow()
        self.proceduresSettingsUi.setWindowModality(Qt.ApplicationModal)
        self.proceduresSettingsUi.show()

    def procedureAutoRunClicked(self):
        # 规程自动运行
        if not self.procedureRunPath:
            reply = QMessageBox.question(self, '提示', '请先导入规程！', QMessageBox.Yes)
        elif self.ProcedureThread._isWork or self.ProcedureThread._isPause:
            reply = QMessageBox.question(self, '提示', '有正在运行的线程！', QMessageBox.Yes)
        else:
            if self.procedureRunIndex == 0:
                self.dockBottom.logBrowser.clear()
            self.ProcedureThread = ProcedureThread(parent=self)
            self.ProcedureThread.run_type = 'usecasegroup'
            self.ProcedureThread.start()
            self.log.infoLog(f'{self.procedureRunPath}规程开始执行')

    def procedureDebugClicked(self):
        # 规程单步执行
        if not self.procedureRunPath:
            reply = QMessageBox.question(self, '提示', '请先导入规程！', QMessageBox.Yes)
        #elif self.procedureRunIndex == self.dockTop.ExcelTab.currentWidget().proListView.colsLen:
            #self.dockTop.ExcelTab.currentWidget().proListView.changeRowColor(-self.procedureRunIndex + 1)
            #self.procedureQuitClicked()
            #self.procedureRunIndex = 0
            #self.ProcedureThread.save_run_result()
            #reply = QMessageBox.question(self, '提示', '已全部执行完毕！', QMessageBox.Yes)
        elif self.ProcedureThread._isWork and not self.ProcedureThread._isPause:
            reply = QMessageBox.question(self, '提示', '有正在自动运行的线程！', QMessageBox.Yes)
        else:
            if self.procedureRunIndex > self.ProcedureThread.procedureExcel.colsLen - 1:
                self.ProcedureThread.run_result = True
                if self.ProcedureThread.procedureExcel.model.item(0,5).text() == '高速':
                        #result = MainWindowConfig.IOMapping.receive_data()
                        #self.tList+=[float(x) for x in list(result)]
                    self.ProcedureThread.atList.append(self.ProcedureThread.tList)
                    self.ProcedureThread.tList = []
                    self.ProcedureThread.endHighPro()
                        #print(result)
                self.ProcedureThread.save_run_result()
                self.ProcedureThread.msleep(MainWindowConfig.RunInterval)
                #self.ProcedureThread.mutex.unlock()
                self.procedureRunIndex = 0
                #self.procedureQuitClicked()
                return
            if self.procedureRunIndex == 0:
                self.dockBottom.logBrowser.clear()
            self.ProcedureThread.judgeIndex = [6, 6]
            if hasattr(self.ProcedureThread, 'procedureExcel'):
                res = self.ProcedureThread.performAction(
                    self.ProcedureThread.procedureExcel.getRowContent(self.procedureRunIndex),self.ProcedureThread.procedureExcel.model.item(self.procedureRunIndex,3).text())
                self.ProcedureThread.procedureExcel.changeRowColor(self.procedureRunIndex, res)
            else:
                res = self.ProcedureThread.performAction(
                    self.dockTop.ExcelTab.currentWidget().proListView.getRowContent(self.procedureRunIndex), self.dockTop.ExcelTab.currentWidget().proListView.model.item(self.procedureRunIndex,3).text())
                self.dockTop.ExcelTab.currentWidget().changeRowColor(self.procedureRunIndex, res)
                self.ProcedureThread.procedureExcel = self.dockTop.ExcelTab.currentWidget().proListView
            self.dockBottom.updateLog(self.procedureRunIndex)
            self.procedureRunIndex += 1

    def procedurePauseClicked(self):
        # 暂停/继续规程
        if not self.ProcedureThread._isWork:
            reply = QMessageBox.question(self, '提示', '没有正在运行的线程！', QMessageBox.Yes)
        elif self.ProcedureThread._isPause:
            self.ProcedureThread.resume()
            self.log.infoLog(f'{self.procedureRunPath}规程继续执行')
        else:
            self.ProcedureThread.pause()
            self.ProcedureThread.is_stop = 1
            self.ProcedureThread.save_run_result()
            self.ProcedureThread.is_stop = 0
            self.log.infoLog(f'{self.procedureRunPath}规程暂停执行')

    def procedureQuitClicked(self):
        # 退出规程
        if self.ProcedureThread._isPause:
            self.ProcedureThread.resume()
        self.ProcedureThread.save_run_result()
        self.procedureRunIndex = 0
        self.ProcedureThread._isWork = False
        self.log.infoLog(f'退出{self.procedureRunPath}')

    def procedureListPauseClicked(self):
        self.procedureListPauseUi = termination(self)
        self.procedureListPauseUi.setWindowModality(Qt.ApplicationModal)
        self.procedureListPauseUi.show()

    # def propertySettingsClicked(self):
    #     print('okk')

    def variableSettingsClicked(self):
        from DcsUi.VariableSettings import VariableSettingsUi
        self.variableSettingsUi = VariableSettingsUi()
        self.variableSettingsUi.projectPath = self.projectPath
        self.variableSettingsUi.show()

    def logRunResultClicked(self):
        self.logRunResultUi = textRecordWindow()
        self.logRunResultUi.setWindowModality(Qt.ApplicationModal)
        self.logRunResultUi.show()

    def logOperateClicked(self):
        # pass
        self.log.show()

    def accountManagementClicked(self):
        self.AccountManagementUi = AccountManage()
        self.AccountManagementUi.setWindowModality(Qt.ApplicationModal)
        self.AccountManagementUi.show()

    def active_update(self):
        self.dockLeft.refreshTree()

    def communicationClicked(self):
        # self.communicationUi = comWindow()
        # self.communicationUi.show()
        pass

    def pharseManagementClicked(self):
        self.PhraseUI = PhraseUI()
        self.PhraseUI.setWindowModality(Qt.ApplicationModal)
        self.PhraseUI.show()

    def addSystemTray(self):
        ''' 添加程序最小化到托盘 '''
        if self.__class__.__name__ == 'MainWindow':
            minimizeAction = QAction("最小化至托盘", self, triggered=self.hide)
            maximizeAction = QAction("最大化", self,
                                     triggered=self.showMaximized)
            restoreAction = QAction("还原", self,
                                    triggered=self.showNormal)
            quitAction = QAction("退出", self,
                                 triggered=self.close)
            self.trayIconMenu = QMenu(self)
            self.trayIconMenu.addAction(minimizeAction)
            self.trayIconMenu.addAction(maximizeAction)
            self.trayIconMenu.addAction(restoreAction)
            self.trayIconMenu.addSeparator()
            self.trayIconMenu.addAction(quitAction)
            self.trayIcon = QSystemTrayIcon(self)
            self.trayIcon.setIcon(QIcon(":/static/default.png"))
            self.trayIcon.setContextMenu(self.trayIconMenu)
            self.trayIcon.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.initUI()
    ex.show()
    sys.exit(app.exec_())
