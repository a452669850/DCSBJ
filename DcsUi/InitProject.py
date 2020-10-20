# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'initproject.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append('../')
from static.Png import *
from DcsUi.CDrawer import CDrawer
from tools.JsonConfig import getProjectList, getProjectName
from utils.InitDb import judgeProjectPath
from utils.AcountModels import User
from mainwindow import MainWindow
from tools.JsonConfig import writeJson, rewriteJson, getProjectPath, getLastUser
from utils.ClientModels import database_proxy
from utils.InitDb import connectDb,judgeProjectPath, initDatabase, createConfig
from peewee import *
import os
import sys
import json
import winreg

def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]
    # return ''


class DrawerWidget(QtWidgets.QWidget):

    def __init__(self, winType = None, projectPath = None, parent = None, *args, **kwargs):
        super(DrawerWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('DrawerWidget{background:white;}')
        self.projectPath = projectPath
        self.winType = winType
        self.parent = parent

        if self.winType == 'Create':
           
            self.gridLayout = QtWidgets.QGridLayout(self)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            # self.lineEdit_2 = QtWidgets.QLineEdit(self)
            self.pathEdit = QtWidgets.QLineEdit(self)
            self.nameEdit = QtWidgets.QLineEdit(self)
            # self.lineEdit_2.setObjectName("lineEdit_2")
            # self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
            self.gridLayout.addWidget(self.pathEdit, 4, 1, 1, 1)
            self.gridLayout.addWidget(self.nameEdit, 3, 1, 1, 1)
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
            # self.pushButton_2 = QtWidgets.QPushButton(self)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            # sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
            # self.pushButton_2.setSizePolicy(sizePolicy)
            # self.pushButton_2.setStyleSheet("background-color:transparent")
            # self.pushButton_2.setText("")
            icon = QtGui.QIcon()
            # icon.addPixmap(QtGui.QPixmap(":/static/createProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            # self.pushButton_2.setIcon(icon)
            # self.pushButton_2.setObjectName("pushButton_2")
            # self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
            # self.label_2 = QtWidgets.QLabel(self)
            # self.label_2.setObjectName("label_2")
            # self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
            self.nameLabel = QtWidgets.QLabel(self)
            self.nameLabel.setObjectName("label_3")
            self.gridLayout.addWidget(self.nameLabel, 3, 0, 1, 1)
            self.pathLabel = QtWidgets.QLabel(self)
            self.pathLabel.setObjectName("label_4")
            self.gridLayout.addWidget(self.pathLabel, 4, 0, 1, 1)

            # self.lineEdit = QtWidgets.QLineEdit(self)
            # self.lineEdit.setObjectName("lineEdit")
            # self.lineEdit.setText('127.0.0.1')
            # self.lineEdit_2.setText('19114')
            # self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
            self.label = QtWidgets.QLabel(self)
            self.label.setObjectName("label")
            self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
            self.gridLayout.setColumnStretch(0, 1)
            self.gridLayout.setColumnStretch(1, 2)
            self.pushButton = QtWidgets.QPushButton()
            self.pushButton.setGeometry(QtCore.QRect(50, 100, 93, 28))
            self.pushButton.setObjectName("pushButton")
            self.pushButton.setStyleSheet("background-color:transparent")
            con = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/static/1209037.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton.setIcon(icon)
            self.gridLayout.addWidget(self.pushButton, 4, 2, 1, 1)
            # self.pushButton_2.clicked.connect(self.chooseDir)
            self.pushButton.clicked.connect(self.createProject)
            # self.createProject()
        elif self.winType == 'Reopen' or self.winType == 'open':
            self.gridLayout = QtWidgets.QGridLayout(self)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            self.lineEdit_2 = QtWidgets.QLineEdit(self)

            self.lineEdit_2.setObjectName("lineEdit_2")
            self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            icon = QtGui.QIcon()
            self.label_2 = QtWidgets.QLabel(self)
            self.label_2.setObjectName("label_2")
            self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
            self.nameLabel = QtWidgets.QLabel(self)
            self.nameLabel.setObjectName("label_3")
            self.gridLayout.addWidget(self.nameLabel, 3, 0, 1, 1)
            self.pathLabel = QtWidgets.QLabel(self)
            self.pathLabel.setObjectName("label_4")
            self.gridLayout.addWidget(self.pathLabel, 4, 0, 1, 1)

            self.lineEdit = QtWidgets.QLineEdit(self)
            self.lineEdit.setObjectName("lineEdit")
            self.lineEdit.setText('127.0.0.1')
            self.lineEdit_2.setText('19114')
            self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
            self.label = QtWidgets.QLabel(self)
            self.label.setObjectName("label")
            self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
            self.gridLayout.setColumnStretch(0, 1)
            self.gridLayout.setColumnStretch(1, 2)
            self.pushButton = QtWidgets.QPushButton()
            self.pushButton.setGeometry(QtCore.QRect(50, 100, 93, 28))
            self.pushButton.setObjectName("pushButton")
            self.pushButton.setStyleSheet("background-color:transparent")
            con = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/static/1209037.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton.setIcon(icon)
            self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
            if self.winType == 'Reopen':
                self.pushButton.clicked.connect(self.reOpenProject)
            else:
                self.pushButton.clicked.connect(self.openProject)

        else:
            self.gridLayout = QtWidgets.QGridLayout(self)
            self.gridLayout.setContentsMargins(1, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            self.pwdIcon = QtWidgets.QLabel(self)
            self.pwdIcon.setMaximumSize(QtCore.QSize(31, 31))
            self.pwdIcon.setText("")
            self.pwdIcon.setPixmap(QtGui.QPixmap(":/static/password.png"))
            self.pwdIcon.setScaledContents(True)
            self.pwdIcon.setObjectName("pwdIcon")
            self.gridLayout.addWidget(self.pwdIcon, 3, 1, 1, 1)
            self.userEdit = QtWidgets.QLineEdit()
            self.userEdit.setMinimumSize(QtCore.QSize(181, 31))
            self.userEdit.setObjectName("userEdit")
            self.gridLayout.addWidget(self.userEdit, 2, 2, 1, 1)
            self.userIcon = QtWidgets.QLabel()
            self.userIcon.setMaximumSize(QtCore.QSize(31, 31))
            self.userIcon.setText("2")
            self.userIcon.setPixmap(QtGui.QPixmap(":/static/user.png"))
            self.userIcon.setScaledContents(True)
            self.userIcon.setObjectName("userIcon")
            self.gridLayout.addWidget(self.userIcon, 2, 1, 1, 1)
            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
            self.loginButton = QtWidgets.QPushButton()
            self.loginButton.setMinimumSize(QtCore.QSize(0, 31))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/static/login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.loginButton.setIcon(icon)
            self.loginButton.setObjectName("loginButton")
            self.loginButton.clicked.connect(self.login)
            self.gridLayout.addWidget(self.loginButton, 5, 1, 1, 2)
            spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem2, 6, 2, 1, 1)
            self.pwdEdit = QtWidgets.QLineEdit()
            self.pwdEdit.setMinimumSize(QtCore.QSize(181, 31))
            self.pwdEdit.setObjectName("pwdEdit")
            self.pwdEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.gridLayout.addWidget(self.pwdEdit, 3, 2, 1, 1)
            spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem3, 4, 2, 1, 1)
            spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem4, 7, 2, 1, 1)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        

    def retranslateUi(self, Form):
        if self.winType == 'Create':
            _translate = QtCore.QCoreApplication.translate
            # self.label_2.setText(_translate("Form", "端口号:"))
            self.nameLabel.setText(_translate("Form", "工程名:"))
            self.pathLabel.setText(_translate("Form", "路径:"))
            # self.label.setText(_translate("Form", "地址:"))
            self.pushButton.setText(_translate("Form", ""))
        elif self.winType == 'Reopen' or self.winType == 'open':
            _translate = QtCore.QCoreApplication.translate
            self.label_2.setText(_translate("Form", "端口号:"))
            self.label.setText(_translate("Form", "地址:"))
        else:
            self.loginButton.setText("登录")

    def login(self):
        if self.projectPath:
            dbPath = os.path.join(self.projectPath, '.resources', 'dcs.db')
            db = SqliteDatabase(dbPath)
            database_proxy.initialize(db)
            db.connect()
        if not User.get_user_by_username('admin'):
            User.create_user('admin', 'admin')
        self.user = self.userEdit.text()
        self.password = self.pwdEdit.text()
        if User.password_valid(self.password) and User.username_valid(self.user):
            user = User.get_or_none(User.username == self.user)
            if user:
                if user.verify_password(self.password):
                    rewriteJson(self.user)
                    # if not hasattr(self, 'createDrawer'):
                    # openCDrader = DrawerWidget(winType = 'open', parent = self.parent)
                    # openCDrader.projectPath = self.projectPath
                    # openCDrader.pushButton.clicked.connect(openCDrader.openProject)
                    # self.parent.createDrawer = CDrawer(self, widget=openCDrader)
                    # self.parent.createDrawer.user = self.user
                    # self.parent.createDrawer.setDirection(CDrawer.RIGHT)
                    # self.parent.createDrawer.setWindowModality(QtCore.Qt.ApplicationModal)
                    # self.parent.createDrawer.show()
                    # self.close()
                    self.showMainwindow()
                    self.close()
                else:
                    reply = QtWidgets.QMessageBox.question(self, '提示', '账户或密码错误！', QtWidgets.QMessageBox.Yes)
            else:
                reply = QtWidgets.QMessageBox.question(self, '提示', '用户不存在！', QtWidgets.QMessageBox.Yes)
        else:
            reply = QtWidgets.QMessageBox.question(self, '提示', '账户或密码错误！', QtWidgets.QMessageBox.Yes)

    def showMainwindow(self):
        self.MainWindow = MainWindow()
        self.MainWindow.projectName = getProjectName(self.projectPath)
        self.MainWindow.projectPath = self.projectPath
        self.MainWindow.user = self.user
        # self.MainWindow.uri = uri
        self.MainWindow.initUI()
        self.MainWindow.show()
        self.parent.close()
        writeJson(self.projectPath)

    # def chooseDir(self):
    #     self.dirPath = QtWidgets.QFileDialog.getExistingDirectory(self,'选择文件夹','./')
    #     self.lineEdit.setText(self.dirPath)
    #     self.show()

    def createProject(self):
        # self.ip = self.lineEdit.text()
        # self.port = self.lineEdit_2.text()
        self.projectPath = self.pathEdit.text()
        self.name = self.nameEdit.text()
        try:
            if not self.user:
                self.user = 'admin'
        except:
            self.user = 'admin'

        if self.projectPath and self.name:
            # if self.ip and self.port:
                # if not os.listdir(self.projectPath):  
                #     self.dbPath = os.path.join(self.projectPath, '.resources', 'dcs.db')
                #     createConfig(self.projectPath, self.projectName)
                #     initDatabase(self.dbPath)
                #     self.showMainwindow()
                #     self.parent.close()
                # else:
                #     reply = QtWidgets.QMessageBox.question(self, '提示', '输入地址！', QtWidgets.QMessageBox.Yes)
                # self.projectPath = os.path.join(get_desktop(),'demo')
                # if not os.path.exists(self.projectPath):
                #     os.makedirs(self.projectPath)
                # else:
                #     self.showMainwindow(self.ip + ':' + self.port)
                #     self.parent.close()
         
            self.dbPath = os.path.join(self.projectPath, '.resources', 'dcs.db')
            createConfig(self.projectPath, self.name)
            initDatabase(self.dbPath)
            self.showMainwindow()
            self.parent.close()
            # else:
            #     reply = QtWidgets.QMessageBox.question(self, '提示', '请输入正确的地址！', QtWidgets.QMessageBox.Yes)
        else:
            reply = QtWidgets.QMessageBox.question(self, '提示', '工程名或路径不可为空！', QtWidgets.QMessageBox.Yes)

    def reOpenProject(self):
        self.projectPath = getProjectPath()
        self.ip = self.lineEdit.text()
        self.port = self.lineEdit_2.text()
        self.user = getLastUser()
        self.showMainwindow()
        self.parent.close()

    def openProject(self):
        # self.projectPath = getProjectPath()
        self.ip = self.lineEdit.text()
        self.port = self.lineEdit_2.text()
        self.user = getLastUser()
        self.showMainwindow()
        self.parent.close()


class Ui_InitProject(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_InitProject, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowIcon(QtGui.QIcon(':/static/default.png'))
        self.setObjectName("InitProject")
        self.resize(872, 644)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 841, 651))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 设置list结构 
        self.listView = QtWidgets.QListView(self.horizontalLayoutWidget)
        self.listView.setObjectName("listView")
        self.model = QtCore.QStringListModel()
        self.projectList = [getProjectName(x) + '\r\n' + self.getShortPath(x) for x in getProjectList() if getProjectName(x)]
        self.projectPathList = [x for x in getProjectList() if getProjectName(x)]
        #设置模型列表视图，加载数据列表
        self.model.setStringList(self.projectList)
        #设置列表视图的模型
        self.listView.setModel(self.model)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setFont(QtGui.QFont( "Timers", 10,  QtGui.QFont.Bold))
        self.listView.setStyleSheet('QListView::item{height:40px;}')
        self.listView.doubleClicked.connect(self.listClicked)
        # self.listView.setItemAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.listView)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logoLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.logoLabel.setText("")
        self.logoLabel.setTextFormat(QtCore.Qt.AutoText)
        self.logoLabel.setPixmap(QtGui.QPixmap(":/static/icon.png"))
        self.logoLabel.setScaledContents(False)
        self.logoLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.verticalLayout.addWidget(self.logoLabel)
        self.titleLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("华文细黑")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.versionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.versionLabel.setFont(font)
        self.versionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.verticalLayout.addWidget(self.versionLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.createButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.createButton.setFont(font)
        self.createButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.createButton.setStyleSheet("background-color:transparent")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/static/createProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createButton.setIcon(icon)
        self.createButton.setObjectName("createButton")
        self.verticalLayout.addWidget(self.createButton)
        self.createButton.clicked.connect(self.createProject)

        self.OpenButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.OpenButton.setFont(font)
        self.OpenButton.setStyleSheet("background-color:transparent")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/static/openProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OpenButton.setIcon(icon1)
        self.OpenButton.setObjectName("OpenButton")
        self.verticalLayout.addWidget(self.OpenButton)
        self.OpenButton.clicked.connect(self.openProject)

        self.reopenButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reopenButton.sizePolicy().hasHeightForWidth())
        self.reopenButton.setSizePolicy(sizePolicy)
        self.reopenButton.setFont(font)
        self.reopenButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.reopenButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.reopenButton.setAutoFillBackground(False)
        self.reopenButton.setStyleSheet('background-color:transparent')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/static/reOpen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reopenButton.setIcon(icon2)
        self.reopenButton.setAutoDefault(False)
        self.reopenButton.setObjectName("reopenButton")
        self.verticalLayout.addWidget(self.reopenButton)
        self.reopenButton.clicked.connect(self.reOpen)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 3)
        self.verticalLayout.setStretch(5, 3)
        self.verticalLayout.setStretch(7, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(2, 5)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("InitProject", "Dcs自动化测试管理软件"))
        self.titleLabel.setText(_translate("InitProject", "DCS自动化测试管理软件"))
        self.versionLabel.setText(_translate("InitProject", "Version 2019"))
        self.createButton.setText(_translate("InitProject", "新建工程"))
        self.OpenButton.setText(_translate("InitProject", "打开工程"))
        self.reopenButton.setText(_translate("InitProject", "恢复上次打开的工程"))

    def createProject(self):
        wid = DrawerWidget(winType = 'Create', parent = self)
        self.dirPath = QtWidgets.QFileDialog.getExistingDirectory(self,'选择文件夹','./')
        if not hasattr(self, 'createDrawer'):
            wid.pathEdit.setText(self.dirPath)
            self.createDrawer = CDrawer(self, widget=wid)
            self.createDrawer.setDirection(CDrawer.RIGHT)
            self.createDrawer.setWindowModality(QtCore.Qt.ApplicationModal)
        self.createDrawer.show()

    def getShortPath(self, path):
            # if 'Desktop' in path:
            #     return '/'.join(path.split('/')[path.split('/').index('Desktop'):])
            # else:
            #     return path
            if path:
                return '/'.join(['～'] + path.split('/')[-2:])

    def listClicked(self, qModelIndex):
        projectPath = self.projectPathList[qModelIndex.row()]
        if judgeProjectPath(projectPath):
            if not hasattr(self, 'loginDrawer'):
                self.loginDrawer = CDrawer(self, widget=DrawerWidget(winType = 'Login', projectPath = projectPath, parent = self))
                self.loginDrawer.setDirection(CDrawer.RIGHT)
                self.loginDrawer.setWindowModality(QtCore.Qt.ApplicationModal)
            self.loginDrawer.projectPath = projectPath
            self.loginDrawer.show()
        else:
            reply = QtWidgets.QMessageBox.question(self, '提示', '路径已失效！', QtWidgets.QMessageBox.Yes)


    def openProject(self):
        self.projectPath = QtWidgets.QFileDialog.getExistingDirectory(self,'选择文件夹','./')
        if judgeProjectPath(self.projectPath):
            if not hasattr(self, 'loginDrawer'):
                login = DrawerWidget(winType = 'Login', parent = self)
                login.projectPath = self.projectPath
                self.loginDrawer = CDrawer(self, widget=login)
                self.loginDrawer.setDirection(CDrawer.RIGHT)
            else:
                self.loginDrawer.projectPath = self.projectPath
            self.loginDrawer.show()
            self.loginDrawer.setWindowModality(QtCore.Qt.ApplicationModal)
        else:
            if self.projectPath:
                reply = QtWidgets.QMessageBox.question(self, '提示', '请选择正确的路径！', QtWidgets.QMessageBox.Yes)

    def reOpen(self):
        self.projectPath = getProjectPath()
        if judgeProjectPath(self.projectPath):
            self.mainWindow = MainWindow()
            self.mainWindow.projectPath = self.projectPath
            self.mainWindow.user = getLastUser()
            self.mainWindow.initUI()
            self.mainWindow.show()
            self.close()
            # if not hasattr(self, 'createDrawer'):
            #     self.createDrawer = CDrawer(self, widget=DrawerWidget(winType = 'Reopen', parent = self))
            #     self.createDrawer.setDirection(CDrawer.RIGHT)
            #     self.createDrawer.setWindowModality(QtCore.Qt.ApplicationModal)
            # self.createDrawer.show()
        else:
            reply = QtWidgets.QMessageBox.question(self, '提示', '上次打开的工程已失效！', QtWidgets.QMessageBox.Yes)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_InitProject()
    mainWindow.show()
    sys.exit(app.exec_())