import typing
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDockWidget, QTreeView, QTabWidget, QListView, QWidget, QHBoxLayout, QLineEdit,\
    QPushButton, QLabel, QCheckBox, QVBoxLayout, QFrame, QMainWindow
from DcsUi.DockCLass import NewDockWidget
from utils.ClientModels import Procedure, Usecase, UsecaseGroup
from procedure.run_procedure.RunProceduree import ProcedureThread
from tools.JsonConfig import getProTree
from static.Png import *
import json
import os

tabelDict = {
        '规程' : Procedure,
        '用例组' : UsecaseGroup,
        '用例' : Usecase,
        }

class TreeDockWidget(NewDockWidget):
    def __init__(self, title, parent = None):
        NewDockWidget.__init__(self, title, parent=parent)
        self.parent = parent
        print(self.__class__.__name__)
        if self.parent.__class__.__name__ != 'MainWindow':
            return
        self.tree = QTreeView(self)
        # 隐藏标题栏
        self.tree.setHeaderHidden(True)
        self.model = TreeDockModel(self.parent)
        self.tree.setModel(self.model)

        self.proListWidget = proListWidget(MainWindow = parent)

        self.listview = self.proListWidget.listView


        self.tab = QTabWidget()
        self.tab.addTab(self.tree, "  规程  ")
        self.tab.addTab(self.proListWidget, "实验列表")
        
        # self.setWidget(self.tree)
        self.setWidget(self.tab)
        self.tree.expandAll()
        self.tree.doubleClicked.connect(self.onTreeClicked)
        self.treeDict = getProTree(self.parent.projectPath)

    def insertProToJson(self,dic,proName):
        if not dic:
            return
        parentName = self.tree.currentIndex().data()
        # print(parentName)
        for key, value in dic.items():
            if key == 'name' and value == parentName:
                l = dic['children']
                proDict = {
                'name' : proName,
                'children' : []
                }
                l.append(proDict)
                # print(l)
                r = []
                for i in l:
                    if i not in r:
                        # print(i['name'])
                        # print([x['name'] for x in r])
                        r.append(i)
                # print(r,l)
                dic['children'] = r
                return dic
            else:
                # if dic:
                if dic['children'] != []:
                    # for d in dic['children']:
                    #     newDict = self.insertProToJson(d,proName)
                    a = []
                    for x in dic['children']:
                        a.append(self.insertProToJson(x, proName))
                    # print(a)
                    dic['children'] = a
                else:
                    return dic
        return dic



    def onTreeClicked(self, index: QModelIndex):
        if  index.parent().data() not in [self.parent.projectName, None]:
            try:
                self.parent.runCountEdit = self.proListWidget.runCountEdit
                # Procedure.get(name = index.data())
                self.parent.proType = Procedure.get(name = index.data()).type
                # self.parent.dockTop.addExcel(index.data())
                self.proListWidget.listView.addItems(index.data())
                self.parent.currentPro = index.data()
                self.parent.procedureRunPath = index.data()
            except:
                # print(1)
                pass
            # if index.parent().data() == '规程':
            #     tabelDb = tabelDict[index.parent().data()]
            #     for x in tabelDb.get_all().where(tabelDb.name == index.data()):
            #         self.parent.procedureRunPath = x.path
            #         self.parent.dockTop.addExcel(x.path)
            #         self.parent.dockBottom.setMaximumHeight(1000)
            # elif index.parent().data() == '用例':
            #     self.parent.dockTop.addUseCase(index.data())
            #     self.parent.procedureRunPath = index.data()
            # elif index.parent().data() == '用例组': 
            #     self.parent.dockTop.addUsecaseGroup(index.data())
            #     self.parent.procedureRunPath = index.data()

    def refreshTree(self):
        self.model.updateData()
        self.tree.expandAll()

class TreeItem(object):
    # 重写树item类
    def __init__(self):
        self.children = []
    
    def appendChild(self, child: 'TreeItem') -> None:
        child.parent = self
        self.children.append(child)

class TreeDockModel(QAbstractItemModel):
    def __init__(self, MainWindow):
        QAbstractItemModel.__init__(self)
        self.rootItem = None
        self.MainWindow = MainWindow
        self.updateData()

    def data(self, index=QModelIndex(), role=Qt.DisplayRole):
        if not index.isValid():
            return None
        # 显示图标
        # if role == Qt.DecorationRole and index.column() == 0:
        #     return QIcon()
        # 显示数据
        if role == Qt.DisplayRole:
            item: TreeItem = index.internalPointer()
            item.data = index.internalPointer().data
            return item.data
        return None

    def updateData(self):
        # 添加规程， 用例等节点
        self.treeDict = getProTree(self.MainWindow.projectPath)
        if self.rootItem:
            self.rootItem = None
        self.rootItem = TreeItem()
        self.rootItem.data = 'Root'
        # self.projectRoot = TreeItem()
        # self.projectRoot.data = self.MainWindow.projectName
        # self.rootItem.appendChild(self.projectRoot)
        # primary = TreeItem()
        # primary.data = self.treeDict['name']
        # primary.parent = self.rootItem
        # self.rootItem.appendChild(primary)
        self.addChild(self.rootItem)
        self.layoutChanged.emit()

    def addChild(self,parent):
        # 添加子节点
        # allList = [x.name for x in tabelDict[tabelName].get_all()]
        for node1 in self.treeDict['children']:
            child1 = TreeItem()
            child1.data = node1['name']
            child1.parent = parent
            parent.appendChild(child1)
            if node1['children'] == [] or None:
                continue
            for node2 in node1['children']:
                child2 = TreeItem()
                child2.data = node2['name']
                child2.parent = child1
                child1.appendChild(child2)
                if node2['children'] == [] or None:
                    continue
                for node3 in node2['children']:
                    child3 = TreeItem()
                    child3.data = node3['name']
                    child3.parent = child2
                    child2.appendChild(child3)
                    if node3['children'] == [] or None:
                        continue
                    for node4 in node3['children']:
                        child4 = TreeItem()
                        child4.data = node4['name']
                        child4.parent = child3
                        child3.appendChild(child4)
                        if node4['children'] == [] or None:
                            continue
                        for node5 in node4['children']:
                            child5 = TreeItem()
                            child5.data = node5['name']
                            child5.parent = child4
                            child4.appendChild(child5)
                            if node5['children'] == [] or None:
                                continue
                # if tabelName == '用例组':
                #     for chilData in json.loads(tabelDict[tabelName].select().where(tabelDict[tabelName].name == child.data)[0].usecase):
                #         usecaseChild = TreeItem()
                #         usecaseChild.data = chilData
                #         usecaseChild.parent = child
                #         child.appendChild(usecaseChild)


    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemIsAutoTristate
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsAutoTristate

    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem: TreeItem = self.rootItem
        else:
            parentItem: TreeItem = parent.internalPointer()
        if row < len(parentItem.children):
            childItem = parentItem.children[row]
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()
        child = index.internalPointer()
        parent = child.parent
        # if not index.isValid():
        #     parent.index = QModelIndex()
        if parent == self.rootItem:
            return QModelIndex()
        return self.createIndex(index.row(), 0, parent)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 1

    def rowCount(self, parent=QModelIndex()) -> int:
        return 999

class CustomWidget(QWidget):

    def __init__(self, text, listview, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(QLabel(text, self))
        self.cb1 = QCheckBox(text, self)
        layout.addWidget(self.cb1)
        self.cb1.clicked.connect(self.cbchange)
        self.listview = listview
        self.text = text

    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)

    def cbchange(self):
        if self.cb1.checkState() == Qt.Checked:
            self.listview.allCbSet.add(self.text)
        else:
            self.listview.allCbSet.remove(self.text)
        # print(self.listview.allCbSet)
        if self.listview.allCbSet:
            self.listview.MainWindow.dockTop.addUsecaseGroup(self.listview.allCbSet)
            groupName = ' - '.join(self.listview.allCbSet)
            self.listview.MainWindow.dockTop.ExcelTab.currentWidget().proListView.groupName = groupName
            self.createGroup(groupName, list(self.listview.allCbSet))
            self.listview.allCbSet.clear()

    def createGroup(self, text, lis):
        usecasegroup = UsecaseGroup()
        usecasegroup.name = text  # 自己填写的用例组的名称
        usecasegroup.usecase = json.dumps(lis)
        usecasegroup.usecase_group_number = text
        check_usecasegroup = None
        try:
            check_usecasegroup = UsecaseGroup.get(UsecaseGroup.name == text)
        except:
            pass
        if check_usecasegroup:
            UsecaseGroup.delete_obj(check_usecasegroup.id)
            usecasegroup.save()
        else:
            usecasegroup.save()


class CheckListView(QListView):

    def __init__(self,MainWindow, *args, **kwargs):
        super(CheckListView, self).__init__(*args, **kwargs)
        self.MainWindow = MainWindow
        # 模型
        self._model = QStandardItemModel(self)
        self.setModel(self._model)
        self.allCbSet = set()
        # 循环生成10个自定义控件
        item = QStandardItem()
        self._model.appendRow(item)  # 添加item

        # # 得到索引
        # index = self._model.indexFromItem(item)
        # widget = CustomWidget(str('全选/全不选'), self)
        # item.setSizeHint(widget.sizeHint())  # 主要是调整item的高度
        # # 设置自定义的widget
        # self.setIndexWidget(index, widget)

    def addItems(self, proName):
        usecaseList = json.loads(Procedure.get(name = proName).usecase)
        # print(type(usecaseList))
        self._model.clear()
        for i in usecaseList:
            print(i)
            item = QStandardItem()
            self._model.appendRow(item)  # 添加item

            # 得到索引
            index = self._model.indexFromItem(item)
            widget = CustomWidget(str(i), self)
            item.setSizeHint(widget.sizeHint())  # 主要是调整item的高度
            # 设置自定义的widget
            self.setIndexWidget(index, widget)



class proListWidget(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.setupUi()

    def setupUi(self):
        from PyQt5 import QtWidgets, QtCore, QtGui
        self.setObjectName("self")
        self.resize(300, 562)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listView = CheckListView(self.MainWindow)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.runCountEdit = QtWidgets.QLineEdit(self)
        self.runCountEdit.setObjectName("runCountEdit")
        self.runCountEdit.setText('1')
        self.horizontalLayout.addWidget(self.runCountEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.label.setText(_translate("Form", " 执行次数："))

 
 
# if __name__ == '__main__':
    
#     app = QApplication(sys.argv)
#     w = AxWidget()
#     w.show()
#     sys.exit(app.exec_())