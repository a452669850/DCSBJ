import datetime
import time
import os
import struct
import sys

import numpy as np
import openpyxl
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from collections import OrderedDict


from utils.WorkModels import PointModel
from Agreement.CS.skio.view.smallwindow import tabWidget

class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values)-min(values)
        #if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600*24:
            string = '%H:%M:%S'
            # label1 = '%b %d -'
            # label2 = ' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = '%d'
            # label1 = '%b - '
            # label2 = '%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = '%b'
            # label1 = '%Y -'
            # label2 = ' %Y'
        elif rng >=3600*24*30*24:
            string = '%Y'
            # label1 = ''
            # label2 = ''
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        # try:
            # label = time.strftime(label1, time.localtime(min(values)))+time.strftime(label2, time.localtime(max(values)))
        # except ValueError:
            # label = ''
        #self.setLabel(text=label)
        return strns

# class CustomViewBox(pg.ViewBox):
#     def __init__(self, window, *args, **kwds):
#         pg.ViewBox.__init__(self, *args, **kwds)
#         self.window = window
#         # self.dic = OrderedDict()
#         # self.dic['h'] = 24
#         # self.dic['0.5h'] = 48
#         # self.dic['15min'] = 96
#         # self.dic['8min'] = 180
#         # self.dic['4min'] = 360
#         # self.dic['2min'] = 720
#         # self.dic['1min'] = 1440
#         # self.l = ['h', '0.5h', '15min', '8min', '4min', '2min', '1min']
#         # self.index = 0
#         # self.RectMode = 3
#         # self.setMouseMode(self.RectMode)

#     # def mouseClickEvent(self, ev):
#     #     if ev.button() == pg.QtCore.Qt.RightButton:
#     #         self.autoRange()

#     def mouseDragEvent(self, ev):
#         pg.ViewBox.mouseDragEvent(self, ev)

#     # def wheelEvent(self, ev, axis=None):
#     #     if ev.delta() == 120:
#     #         if self.window.index == 6:
#     #             pg.ViewBox.wheelEvent(self, ev, axis)
#     #             return
#     #         self.window.index += 1
#     #         tick_x = [str(x) + '/'  for x in range(1, self.dic[self.l[self.window.index]] + 1)]
#     #         self.window.xNum *= 2
#     #         print(self.window.xNum)
#     #         self.window.plotTrend(self.window.curentVar, self.window.xNum, None, tick_x = tick_x)
#     #         pg.ViewBox.wheelEvent(self, ev, axis)
#     #     elif ev.delta() == -120:
#     #         # if self.window.index == 0:
#     #         #     pg.ViewBox.wheelEvent(self, ev, axis)
#     #         #     return
#     #         if self.window.index == 0:
#     #             # pg.ViewBox.wheelEvent(self, ev, axis)
#     #             return
#     #         self.window.index -= 1
#     #         tick_x = [str(x) + '/' + self.l[self.window.index] for x in range(1, self.dic[self.l[self.window.index]] + 1)]
#     #         self.window.xNum //= 2
#     #         print(self.window.xNum)
#     #         self.window.plotTrend(self.window.curentVar, self.window.xNum, None, tick_x = tick_x)
#     #         pg.ViewBox.wheelEvent(self, ev, axis)
#     #     else:
#     #         ev.ignore()

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # self.setMouseMode(self.RectMode)
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
            
    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)

    def wheelEvent(self, ev, axis=None):
        # pg.ViewBox.wheelEvent(self, ev, axis)
        # self.setXRange(0,10) 
        pass


class TrendUi(QtWidgets.QWidget):
    def __init__(self, projectPath,parent=None):
        super(TrendUi, self).__init__(parent)
        self.projectPath = projectPath
        self.getCardIdIndex()
        self.getDic()
        self.setupUi()
        self.xNum = 500
        self.index = 0

    def getDic(self):
        self.dic = {}
        # try:
        self.vl = PointModel.select()
        for x in self.vl:
            self.dic[str([int(x.channel), int(x.reg), x.offset])] = x.sig_name
        # except:
        #     pass

    def getCardIdIndex(self):
        self.D_index = set()
        self.AO_index = set()
        self.AI_index = set()
        for i in PointModel.select():
            if i.sig_type in ('DO', 'DI'):
                self.D_index.add(int(i.channel))
            if i.sig_type == 'AO':
                self.AO_index.add(int(i.channel))
            if i.sig_type == 'AI':
                self.AI_index.add(int(i.channel))

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(1037, 669)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.horizontalLayout_3.addWidget(self.comboBox)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.searchVar)
        self.horizontalLayout_3.addWidget(self.pushButton)
        # self.chooseExcel = QtWidgets.QPushButton(self)
        # self.chooseExcel.setObjectName("excelButton")
        # self.chooseExcel.clicked.connect(self.importExcel)
        # self.horizontalLayout_3.addWidget(self.chooseExcel)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 5)
        self.horizontalLayout_3.setStretch(2, 1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemDoubleClicked.connect(self.listChange)
        self.gridLayout.addWidget(self.listWidget, 2, 0, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.addData()

    # 绘图函数
    def plotTrend(self, curentVar, num, bol):
        self.xAxisIndexList = []
        # self.tick_x = tick_x
        varList = []
        axisList = []
        tick_xv = []
        channel = eval(list(self.dic.keys())[list(self.dic.values()).index(curentVar)])
        # print(channel)
        allVauleList, allTimeList = self.getValues(channel)
        self.getXAxisNumber(self.fileLen, num)
        for i, v in enumerate(allVauleList):
            if i in self.xAxisIndexList:
                try:
                    # print(v,i)
                    varList.append(float(v))
                    tick_xv.append(allTimeList[i])
                except:

                    continue
                # tick_x.append(allTimeList[i])
        # print(allVauleList)
        # if allVauleList[0] >= 1 or allVauleList[0] == 0:
        #     tick_y = [str(x) for x in range(0, 21)]
        # else:
        #     tick_y = ['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']
        tick_x_list = self.getList(1000, 'x')
        # tick_y_list = self.getList(len(tick_y), 'y')
        # ticks_x = [(i, j) for i, j in zip(tick_x_list, tick_x)]
        # ticks_y = [(i, j) for i, j in zip(tick_y_list, tick_y)]
        # ticks_y_dict = {}
        x_Axis = DateAxis(orientation='bottom')
        # y_Axis = pg.AxisItem(orientation='left')
        # x_Axis.setTicks([ticks_x])
        # y_Axis.setTicks([ticks_y])
        vb = CustomViewBox()
        if hasattr(self, 'trendWidget') or not bol:
            self.trendWidget.clear()
        self.trendWidget = pg.PlotWidget(title=f'{curentVar}趋势图', axisItems={'bottom': x_Axis},
                                             viewBox=vb)
        self.gridLayout.addWidget(self.trendWidget, 2, 1, 1, 1)
        x = np.array([x for x in varList], dtype=np.float_)
        # y = np.array([4,5,6], dtype=np.float_)
        # self.trendWidget.plot(y, pen = 'r')
        self.trendWidget.plot(x = tick_xv, y = varList, pen='r')

    # 添加文件到下拉框
    def addData(self):
        # print(self.projectPath)
        try:
            for x in os.listdir(os.path.join(self.projectPath, 'demo')):
                # print(x)
                if x.split('.')[-1] == 'dat':
                    self.comboBox.addItem(x)
        except:
            return

    # 添加所有变量
    def addVar(self):
        # i = 0
        # print(self.dic)
        # with open(self.fileName,"rb") as f: 
        #     for fLine in f:
        #         if i == 1:
        #             # print(fLine)
        #             varList = self.getData(fLine[:-2])
        # for x, i in enumerate(varList):
        #     for y, j in enumerate(i):
        #         try:
        #             varName = self.dic[str([x+1,y+1])]
        #             self.listWidget.addItem(varName)
        #         except:
        #             pass
        # return
        # i += 1
        for k, v in self.dic.items():
            self.listWidget.addItem(v)

    # 下拉框选择
    def selectionchange(self):
        self.fileName = os.path.join(self.projectPath, 'demo', self.comboBox.currentText())
        self.addVar()

    # 双击变量
    def listChange(self, item):
        self.curentVar = item.text()
        self.xNum = 500
        self.plotTrend(self.curentVar, self.xNum, True)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "趋势图"))
        self.pushButton.setText(_translate("Form", "搜索"))
        # self.chooseExcel.setText(_translate("Form", "导入变量表"))
        self.label.setText(_translate("Form", "变量点"))

    # 获取坐标间隔列表
    def getList(self, length, typ):
        n = 0
        if typ == 'x':
            l = []
            for x in range(length):
                n += self.xNum // 1000
                l.append(n)
            return l
        elif typ == 'y':
            l = [0]
            for x in range(length):
                n += 1
                l.append(n)
            return l


    def bitwise(value, PlaceNumber):
        return value >> PlaceNumber

    # 获取所有的时间和值
    def getValues(self, channel):
        index = 0
        values = []
        times = []
        with open(self.fileName, "rb") as f:
            for fLine in f:
                if fLine != b'\n':

                    # print(channel)
                    # print(fLine[:-2],len(fLine[:-2]))
                    if len(fLine[:-2]) == 1248:
                        try:
                            if channel[2]:
                                values.append(
                                    self.get_bit_val(self.getData(fLine[:-2])[channel[1] - 1][channel[0] - 1], channel[2]))
                            else:
                                values.append(self.getData(fLine[:-2])[channel[1] - 1][channel[0] - 1])
                        except:
                            # print(fLine)
                            # continue
                            pass
                    elif len(fLine[:-2]) == 8:
                        try:
                            times.append(struct.unpack('d', fLine[:-2])[0])
                        except:
                            # print(fLine)
                            # continue
                            pass
                index += 1
            self.fileLen = index
            return values, times

    # 递归获取横坐标500个点的索引
    def getXAxisNumber(self, index, number):
        if number == 0:
            return
        interval = 0
        if index % number == 0 and number == index:
            interval = index / number
            return [x for x in list(range(0, index, interval))]
        else:
            interval = index // number + 1
        xAxisNumberList_ = []
        xAxisNumber = 0
        xAxisNumberList = [x for x in list(range(0, index, interval))]
        xAxisNumberList_ = list(set(xAxisNumberList))
        xAxisNumberList_.sort(key=xAxisNumberList.index)
        n = number - len(xAxisNumberList_)
        try:
            self.xAxisIndexList += self.getXAxisNumber(index, n)
        except:
            self.xAxisIndexList += xAxisNumberList_

    def importExcel(self):
        self.excelPath, filetype = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', '',
                                                                         'Excel files(*.xlsx , *.xls)')
        if self.excelPath:
            wb = openpyxl.load_workbook(self.excelPath)
            ws = wb.active
            for row in list(ws.iter_rows())[1:]:
                l = [x.value for x in row]
                PointModel.create(sig_name=row[1].value, type=row[2].value, cabinets=row[3].value, channel=row[4].value,
                                cardID=row[5].value, PlaceNumber=row[7].value)

    def getData(self, res):
        lis = []

        # print(res, len(res))
        b = struct.unpack('64s64s64s64s64s256s128s128s64s144s144s64s', res)
        # print(b)
        for i in b:
            # print(len(i), 22222, i)
            # print(struct.unpack('d' * int((len(i)/8)), i))
            lis.append(struct.unpack('d' * int((len(i)/8)), i))
        # for i in self.D_index:
        #     lis.append(struct.unpack('d' * 8, b[i -1]))
        # for i in (list(self.AI_index) + list(self.AO_index)):
        #     lis.append(struct.unpack('d' * 8, b[i -1]))
        # print(len(data1))
        # struct.unpack('d' * 8, data1)
        # struct.unpack('d' * 40, data1)
        # str1 = ('%ds' % (len(data1) / 24)) * 24
        # data2 = struct.unpack(str1, data1)
        # for i in data2:
        #     data.append(list(struct.unpack('d' * 8, i)))
        # str1 = ('%ds' % (len(data1) / 4)) *4
        # data2 = struct. unpack(str1, data1)
        # for i in data2:
        #     data.append(list(struct.unpack('d' * 8, i)))
        # print(lis)
        return lis

    # def getTime(self, res):
    #     pass

    def searchVar(self):
        text = self.lineEdit.text()
        if text:
            for k, v in self.dic.items():
                # print(k,v)
                if v == text:
                    self.listWidget.clear()
                    self.listWidget.addItem(v)
        else:
            self.addVar()
            # else:
            #     reply = QtWidgets.QMessageBox.question(self, '提示', '没有搜索到变量！', QtWidgets.QMessageBox.Yes)

    def get_bit_val(self, byte, index):
        byte = bin(byte)
        # print(byte, index)
        """
        得到某个字节中某一位（Bit）的值

        :param byte: 待取值的字节值
        :param index: 待读取位的序号，从右向左0开始，0-7为一个完整字节的8个位
        :returns: 返回读取该位的值，0或1
        """
        # print(index)
        if byte & (1 << int(index)):
            return 1
        else:
            return 0


class MainWindowConfig:
    IOMapping = None

    @classmethod
    def setIOMapping(cls, iomapping):
        cls.IOMapping = iomapping


class MainWindow(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.tab1 = tabWidget()
        self.tab2 = TrendUi()
        self.addTab(self.tab1, "实时数据")
        self.addTab(self.tab2, "历史趋势图")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.showMaximized()
    app.exec_()
    # b = format(2, 'b')
    # print(b)
    # print(int(b, 2))
