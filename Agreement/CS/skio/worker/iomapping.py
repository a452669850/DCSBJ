import os
import struct
import time
from pathlib import Path
from PyQt5.QtCore import QTimer

import numpy

from Agreement.CS.skio.define import AOdataPacket, DIdataPacket, AIdataPacket, HSdataPacket
from Agreement.CS.skio.manage import SkIO
from utils.WorkModels import PointModel


class IOMapping:
    def __init__(self, path, uri):
        super().__init__()

        self.skio = SkIO()
        self.skio.setup(uri, Path(os.path.join(path, 'demo')))
        self.D_index = None
        self.AO_index = None
        self.AI_index = None
        self.current_value = []
        # self.current_value1 = None
        # self.current_value2 = None
        # self.current_value3 = None
        # self.current_value4 = None
        self.Packet_serial_No = 0x00000000
        self.setupvalue()

    def setupvalue(self):
        self.DO_index = set()
        self.DI_index = set()
        self.AO_index = set()
        self.AI_index = set()
        self.DO_dic = {}
        self.DI_dic = {}
        self.AO_dic = {}
        self.AI_dic = {}
        self.dic = {}
        for i in PointModel.select():
            if i.sig_type in ('DO-24V', 'DO-48V', 'DO'):
                self.DO_index.add(int(i.reg))
            if i.sig_type in ('DI-24V', 'DI-48V', 'DI'):
                self.DI_index.add(int(i.reg))
            # if i.sig_type == 'AO' or i.sig_type == 'PT100' or i.sig_type == 'TC/T' or i.sig_type == 'RTD' or i.sig_type == 'TC':
            if i.sig_type == 'AO' or i.sig_type == 'PT100' or i.sig_type == 'TC/T' or i.sig_type == 'RTD' or i.sig_type == 'TC/K':
                self.AO_index.add(int(i.reg))
            if i.sig_type == 'AI':
                self.AI_index.add(int(i.reg))
        self.DO_index = sorted(list(self.DO_index))
        self.DI_index = sorted(list(self.DI_index))
        self.AO_index = sorted(list(self.AO_index))
        self.AI_index = sorted(list(self.AI_index))
        self.ALL_index = list(set(self.DO_index + self.DI_index + self.AO_index + self.AI_index))
        for i in self.DO_index:
            self.DO_dic[i] = set()
            for j in PointModel.select().where(PointModel.reg == i):
                if j.sig_type in ('DO-24V', 'DO-48V', 'DO'):
                    self.DO_dic[i].add(int(j.channel))
        for i in self.DI_index:
            self.DI_dic[i] = set()
            for j in PointModel.select().where(PointModel.reg == i):
                if j.sig_type in ('DI-24V', 'DI-48V', 'DI'):
                    self.DI_dic[i].add(int(j.channel))
        for i in self.AO_index:
            self.AO_dic[i] = set()
            for j in PointModel.select().where(PointModel.reg == i):
                # if j.sig_type == 'AO' or j.sig_type == 'PT100' or j.sig_type == 'TC/T' or j.sig_type == 'RTD' or j.sig_type == 'TC':
                if j.sig_type == 'AO' or j.sig_type == 'PT100' or j.sig_type == 'TC/T' or j.sig_type == 'RTD' or j.sig_type == 'TC/K':
                    self.AO_dic[i].add(int(j.channel))
        for i in self.AI_index:
            self.AI_dic[i] = set()
            for j in PointModel.select().where(PointModel.reg == i):
                if j.sig_type == 'AI':
                    self.AI_dic[i].add(int(j.channel))
        for i in self.ALL_index:
            self.dic[i] = set()
            for j in PointModel.select().where(PointModel.reg == i):
                self.dic[i].add(int(j.channel))
        try:
            for z in range(max(self.ALL_index)):
                if z in [i-1 for i in self.ALL_index]:
                    self.current_value.append([0 for x in range(max(self.dic[z+1]))])
                else:
                    self.current_value.append([0 for x in range(8)])
        except:
            return
        # if self.DO_index == []:
        #     self.current_value1 = []
        # else:
        #     self.current_value1 = [self.current_value[i - 1][min(self.DO_dic[i])-1:max(self.DO_dic[i])] for i in self.DO_index]
        # if self.DI_index == []:
        #     self.current_value2 = []
        # else:
        #     self.current_value2 = [self.current_value[i - 1][min(self.DI_dic[i])-1:max(self.DI_dic[i])] for i in self.DI_index]
        # if self.AO_index == []:
        #     self.current_value3 = []
        # else:
        #     self.current_value3 = [self.current_value[i - 1][min(self.AO_dic[i])-1:max(self.AO_dic[i])] for i in self.AO_index]
        # if self.AI_index == []:
        #     self.current_value4 = []
        # else:
        #     self.current_value4 = [self.current_value[i - 1][min(self.AI_dic[i])-1:max(self.AI_dic[i])] for i in self.AI_index]
        self.force_value = {point.sig_name: None for point in PointModel.all_points()}
        self.force_value_stact = {point.sig_name: False for point in PointModel.all_points()}

    # def setupvalue(self):
    #     self.D_index = set()
    #     self.AO_index = set()
    #     self.AI_index = set()
    #     self.AOR_index = set()
    #     for i in PointModel.select():
    #         if i.sig_type in ('DO-24V', 'DO-48V', 'DI-24V', 'DI-48V', 'DO', 'DI'):
    #             self.D_index.add(int(i.reg))
    #         if i.sig_type == 'AO' or i.sig_type == 'PT100' or i.sig_type == 'TC/T':
    #             if '热电偶' in i.slot or 'RTD' in i.slot:
    #                 self.AOR_index.add(int(i.reg))
    #                 continue
    #             self.AO_index.add(int(i.reg))
    #         if i.sig_type == 'AI':
    #             self.AI_index.add(int(i.reg))
    #     self.D_index = sorted(list(self.D_index))
    #     self.AO_index = sorted(list(self.AO_index))
    #     self.AI_index = sorted(list(self.AI_index))
    #     self.AOR_index = sorted(list(self.AOR_index))
    #     self.ALL_index = self.D_index + self.AO_index + self.AI_index
    #     try:
    #         for z in range(max(self.ALL_index)):
    #             if z in [i - 1 for i in self.AO_index]:
    #                 self.current_value.append([0 for x in range(32)])
    #             elif z in [i - 1 for i in self.AOR_index]:
    #                 self.current_value.append([0 for x in range(16)])
    #             else:
    #                 self.current_value.append([0 for x in range(8)])
    #     except:
    #         return
    #     if self.D_index == []:
    #         self.current_value1 = []
    #     else:
    #         self.current_value1 = [self.current_value[i - 1] for i in self.D_index]
    #     if self.AO_index == []:
    #         self.current_value2 = []
    #     else:
    #         self.current_value2 = [self.current_value[i - 1] for i in (self.AO_index + self.AOR_index)]
    #     if self.AI_index == []:
    #         self.current_value3 = []
    #     else:
    #         self.current_value3 = [self.current_value[i - 1] for i in self.AI_index]
    #     self.force_value = {point.sig_name: None for point in PointModel.all_points()}
    #     self.force_value_stact = {point.sig_name: False for point in PointModel.all_points()}

    # 写AO
    def setAOcurrent(self):
        # if self.current_value2 == None:
        #     return
        data1 = []
        lis = [self.current_value[i - 1][min(self.AO_dic[i])-1:max(self.AO_dic[i])] for i in self.AO_index]
        for i in lis:
            for j in i:
                # print(j)
                data1.append(j)
        # print(data1)
        data = AOdataPacket(1, 640, self.Packet_serial_No, data1)
        self.skio.AOwrite(data)
        self.Packet_serial_No += 1
        for i in zip(lis, list(self.AO_index)):
            self.current_value[int(i[-1]) - 1][min(self.AO_dic[i[-1]])-1:max(self.AO_dic[i[-1]])] = i[0]
        self.write_storeData(tim=time.time(), data=self.current_value)

    # 写DO
    def setDIcurrent(self):
        # if self.current_value1 == None:
        #     return
        DO_index = [self.DO_index[-1], self.DO_index[0]]
        data1 = [self.current_value[i - 1][min(self.DO_dic[i])-1:max(self.DO_dic[i])] for i in self.DO_index]
        data1 = [data1[-1],data1[0]]
        print(data1)
        data = DIdataPacket(2, 64, self.Packet_serial_No, data1)
        self.skio.DIwrite(data)
        self.Packet_serial_No += 1
        for i in zip(data1, list(DO_index)):
            self.current_value[int(i[-1]) - 1][min(self.DO_dic[i[-1]])-1:max(self.DO_dic[i[-1]])] = i[0]
        self.write_storeData(tim=time.time(), data=self.current_value)

    # 读AI
    def upAIcurrent(self):
        # # if self.current_value3 == None:
        # #     return
        # data = AIdataPacket(3, 0, self.Packet_serial_No)
        # data1 = self.skio.AIread(data)
        # data2 = list(map(int, average(data1)))
        # data3 = []
        # for i in range(len(data2)):
        #     if i % 8 != 0:
        #         continue
        #     data3.append(data2[i:i+8])
        # # self.current_value3 = [data1[-1][0:8], data1[-1][8:16], data1[-1][16:24]]
        # self.current_value4 = data3
        # self.Packet_serial_No += 1
        # for i in zip(self.current_value4, list(self.AI_index)):
        #     self.current_value[int(i[-1]) - 1][min(self.AI_dic[i[-1]])-1:max(self.AI_dic[i[-1]])] = i[0]
        # if self.current_value3 == None:
        #     return
        data = AIdataPacket(3, 0, self.Packet_serial_No)
        data1 = self.skio.AIread(data)
        data2 = [float(x) for x in average(data1)]
        data2 = getRealAI(data2)

        # data2 = list(data1[0])
        # average
        data3 = []

        # for i in range(len(data2)):
        #     if i % 8 != 0:
        #         continue
        #     data3.append(data2[i:i+8])
        # print(data1,'data1')
        # print(data2,'data2')
        # print(data3,'data3')
        # self.current_value3 = [data1[-1][0:8], data1[-1][8:16], data1[-1][16:24]]
        
        self.current_value4 = data2
        self.Packet_serial_No += 1
        # print(self.AI_index, self.AI_dic, type(data2))
        for i in zip(self.current_value4, list(self.AI_index)):
            # print(i,999999)
            self.current_value[int(i[-1]) - 1][min(self.AI_dic[i[-1]])-1:max(self.AI_dic[i[-1]])] = self.current_value4

    # 读DI
    def upDIcurrent(self):
        # # if self.current_value1 == None:
        # #     return
        # data = AIdataPacket(4, 0, self.Packet_serial_No)
        # data1 = self.skio.DIread(data)
        # data2 = list(map(int, average(data1)))
        # data3 = []
        # for i in range(len(data2)):
        #     if i % 4 != 0:
        #         continue
        #     data3.append(data2[i:i + 4])
        # self.current_value2 = data3
        # self.Packet_serial_No += 1
        # for i in zip(self.current_value2, list(self.DI_index)):
        #     self.current_value[int(i[-1]) - 1][min(self.DI_dic[i[-1]])-1:max(self.DI_dic[i[-1]])] = i[0]
        # # for i in zip(self.current_value2, list(self.DI_index)):
        # #     self.current_value[int(i[-1]) - 1] = i[0]
        # if self.current_value1 == None:
        #     return
        data = AIdataPacket(4, 0, self.Packet_serial_No)
        data1 = self.skio.DIread(data)
        data2 = data1[0]
        # print(data2, len(data2), 'qweqwe')
        data3 = []
        for i in range(len(data2)):
            if i % 4 != 0:
                continue
            data3.append(data2[i:i + 4])
        self.current_value2 = data3
        self.Packet_serial_No += 1
        # print(i)
        # print(self.DI_dic)
        D_index = [self.DI_index[-1], self.DI_index[0]]
        # print(data3)
        for i in zip(self.current_value2, list(D_index)):
            self.current_value[int(i[-1]) - 1][min(self.DI_dic[i[-1]])-1:max(self.DI_dic[i[-1]])] = i[0]
        # for i in zip(self.current_value2, list(self.DI_index)):
        #     self.current_value[int(i[-1]) - 1] = i[0]

    def High_speed_test(self, type, x):
        """下发高速实验命令开始"""
        if self.current_value == []:
            return
        # self.current_value.append(type)
        lis = self.current_value
        # print(lis[9][11:18])
        H_List = []
        H_List+=(lis[9][10:18])
        # print(lis[9][11:18])
        H_List+=(lis[10][10:18])
        # print(lis[10][11:18])
        H_List+=(lis[1][0:8])
        # print(lis[1][0:8])
        H_List+=(lis[2][0:8])
        # print(lis[2][0:8])
        H_List+=(lis[7][0:16])
        # print(lis[7][0:16])
        H_List+=(lis[10][0:4])
        print(lis[10][0:4])
        H_List+=(lis[11][4:8])
        print(lis[11][4:8])
        H_List.append(type)
        print(len(H_List))


        # if len(l2) < 12:
        #     print(len(lis))
        data = HSdataPacket(7, 4, self.Packet_serial_No, H_List)
        # num = self.Packet_serial_No + 1
        # self.skio.start_high_speed_test(data, num)
        self.skio.start_high_speed_test(data)
        self.Packet_serial_No = self.Packet_serial_No + 1

    def receive_data(self):
        """接受高速实验数据"""
        data = self.skio.receive_data()
        # data = self.skio.receive_data()[0]
        # self.Packet_serial_No = self.skio.receive_data()[1]
        return data

    def readall(self):
        if self.current_value == []:
            return
        self.upAIcurrent()
        self.upDIcurrent()
        self.write_storeData(tim=time.time(), data=self.current_value)

    def read(self, name):
        # self.upAIcurrent()
        # self.upDIcurrent()
        point = PointModel.get(PointModel.sig_name == name)
        if point.offset:
            return get_bit_val(self.current_value[int(point.reg) - 1][int(point.channel) - 1], point.offset)
        else:
            return self.current_value[int(point.reg) - 1][int(point.channel) - 1]

    def write(self, name, value):
        point = PointModel.get(PointModel.sig_name == name)
        if point.sig_type in ('DO-24V', 'DO-48V', 'DO'):
            val = self.current_value[int(point.reg) - 1][int(point.channel) - 1]
            value = set_bit_val(byte=val, val=int(value), index=int(point.offset))
        elif point.sig_type == 'AO':
            value = float(value)
        elif point.sig_type == 'TC/K':
            value = TC_K(value)
        elif point.sig_type == 'TC/T':
            value = TC_T(value)
        elif point.sig_type == 'TC/E':
            value = TC_E(value)
        elif point.sig_type == 'PT100':
            value = pt100_t2r(value)

        self.current_value[int(point.reg) - 1][int(point.channel) - 1] = value
        if point.sig_type in ('DO-24V', 'DO-48V', 'DO'):
            self.setDIcurrent()
        elif point.sig_type == 'AO' or point.sig_type == 'PT100' or point.sig_type == 'TC/T' or point.sig_type == 'TC/K':
            self.setAOcurrent()
        return value

    def runWrite(self, name, value):
        point = PointModel.get(PointModel.sig_name == name)
        if point.sig_type in ('DO-24V', 'DO-48V', 'DO'):
            val = self.current_value[int(point.reg) - 1][int(point.channel) - 1]
            value = set_bit_val(byte=val, val=int(value), index=int(point.offset))
        elif point.sig_type == 'AO':
            var = value
            highValue = float(point.rhi)
            lowValue = float(point.rlo)
            var = self.getRealAO(var, highValue, lowValue)
            value = float(var)
        elif point.sig_type == 'TC/K':
            value = TC_K(value)
        elif point.sig_type == 'TC/T':
            value = TC_T(value)
        elif point.sig_type == 'TC/E':
            value = TC_E(value)
        elif point.sig_type == 'PT100':
            value = pt100_t2r(value)

        self.current_value[int(point.reg) - 1][int(point.channel) - 1] = value
        # if point.sig_type in ('DO-24V', 'DO-48V', 'DO'):
        # elif point.sig_type == 'AO' or point.sig_type == 'PT100' or point.sig_type == 'TC/T' or point.sig_type == 'TC/K':
        # self.setDIcurrent()
        # self.setAOcurrent()
        return value

    def getRealAO(self,x,highValue, lowValue):
        if highValue:
            return (16 * (x - lowValue) + 4 * (highValue-lowValue))/(1000 * (highValue - lowValue))
        else:
            return x/1000

    def doWrite(self):
        self.setDIcurrent()
        self.setAOcurrent()

    def GS_write(self, name, value, type):
        print(name, value, type, 3333333333333333333333)
        try:
            point = PointModel.get(PointModel.sig_name == name)
        except Exception as e:
            print(list(name),2222222222222222222222)
            return e
        if point.sig_type in ('DO-24V', 'DO-48V','DO'):
            val = self.current_value[int(point.reg) - 1][int(point.channel) - 1]
            value = set_bit_val(byte=val, val=int(value), index=int(point.offset))
        elif point.sig_type == 'AO':
            highValue = float(point.rhi)
            lowValue = float(point.rlo)
            var = self.getRealAO(value, highValue, lowValue)
            value = float(var)
        elif point.sig_type == 'TC/K':
            value = TC_K(value)
        elif point.sig_type == 'TC/T':
            value = TC_T(value)
        elif point.sig_type == 'TC/E':
            value = TC_E(value)
        elif point.sig_type == 'PT100':
            value = pt100_t2r(value)
        self.current_value[int(point.reg) - 1][int(point.channel) - 1] = value

    def start_gather(self,parent):
        from PyQt5.QtCore import QTimer
        data = AIdataPacket(5, 0, self.Packet_serial_No)
        self.skio.start_gather(data)
        print('低速开始')
        self.timer = QTimer(parent)
        self.timer.start(500)
        self.timer.timeout.connect(self.readall)
        # self.readall()
        self.Packet_serial_No += 1

    def stop_gather(self):
        data = AIdataPacket(6, 0, self.Packet_serial_No)
        print(data, '低速结束')
        self.skio.stop_gather(data)
        try:
            self.timer.stop()
        except:
            pass
        self.Packet_serial_No += 1

    def START_GS_experiment(self):
        """高速实验开始"""
        data = AIdataPacket(9, 0, self.Packet_serial_No)
        print(data, '高速开始')
        self.skio.stop_gather(data)
        self.Packet_serial_No += 1

    def STOP_GS_experiment(self):
        """告诉实验停止"""
        data = AIdataPacket(10, 0, self.Packet_serial_No)
        self.skio.stop_gather(data)
        self.Packet_serial_No += 1

    def write_storeData(self, tim, data):
        lis = []
        # for key in self.DO_dic:
        #     lis.append(struct.pack('Q' * len(self.DO_dic[key]), *data[key - 1][min(self.DO_dic[key])-1:max(self.DO_dic[key])]))
        # for key in self.DI_dic:
        #     lis.append(struct.pack('Q' * len(self.DI_dic[key]), *data[key - 1][min(self.DI_dic[key])-1:max(self.DI_dic[key])]))
        # for key in self.AI_dic:
        #     lis.append(struct.pack('d' * len(self.AI_dic[key]), *data[key - 1][min(self.AI_dic[key])-1:max(self.AI_dic[key])]))
        # for key in self.AO_dic:
        #     lis.append(struct.pack('d' * len(self.AO_dic[key]), *data[key - 1][min(self.AO_dic[key])-1:max(self.AO_dic[key])]))
        for i in data:
            lis.append((struct.pack('d' * len(i), *i)))
        data1 = struct.pack('64s64s64s64s64s256s128s128s64s144s144s64s', *lis)
        self.skio.storeData.write(tim, data1)

def getRealAO(x,highValue, lowValue):
    if highValue:
        return (16 * (x - lowValue) + 4 * (highValue-lowValue))/(1000 * (highValue - lowValue))
    else:
        return x/1000

def get_bit_val(byte, index):
    """
    得到某个字节中某一位（Bit）的值

    :param byte: 待取值的字节值
    :param index: 待读取位的序号，从右向左0开始，0-7为一个完整字节的8个位
    :returns: 返回读取该位的值，0或1
    """
    if byte & (1 << index):
        return 1
    else:
        return 0


def set_bit_val(byte, index, val):
    """
    更改某个字节中某一位（Bit）的值

    :param byte: 准备更改的字节原值
    :param index: 待更改位的序号，从右向左0开始，0-7为一个完整字节的8个位
    :param val: 目标位预更改的值，0或1
    :returns: 返回更改后字节的值
    """
    if val:
        return byte | (1 << index)
    else:
        return byte & ~(1 << index)


def pt100_t2r(t):
    """
    PT100, 温度到电阻转换公式

    从0℃~850℃：
    Rt=R0（1+A*t+B*t^2）

    从-200℃~0℃：
    Rt=R0[1+A*t+Bt^2+C(t-100)*t^3]
    式中：
    Rt----温度为t时的铂电阻的阻值
    R0----温度为0时的铂电阻的阻值，即100Ω

    A=3.9083*10^(-3)℃^(-1)
    B=-5.775*10^(-7) ℃^(-2)
    C=-4.183*10^(-12) ℃^(-4)

    """
    A = 3.9083 * (10 ** -3)
    B = -5.775 * (10 ** -7)
    C = -4.183 * (10 ** -12)
    R0 = 100
    if 0 <= t <= 850:
        Rt = R0 * (1 + A * t + B * t * t)
        return Rt
    elif -200 <= t < 0:
        Rt = R0 * (1 + A * t + B * t * t + C * (t - 100) * t ** 3)
        return Rt
    else:
        raise ValueError("温度超范围 -200 ~ 800 度")


def TC_T(t):
    '''
    https://max.book118.com/html/2018/0907/8061021016001123.shtm
    RTD_T 热电偶 温度转电动势 计算函数
    输入 ： t (摄氏度)
    输出 ： e (毫伏)
    '''
    if -270 <= t <= 0:
        a0 = 0.000_000_000_0 * 10 ** 0
        a1 = 3.874_810_636_4 * 10 ** 1
        a2 = 4.419_443_434_7 * 10 ** -2
        a3 = 1.184_432_310_5 * 10 ** -4
        a4 = 2.003_297_355_4 * 10 ** -5
        a5 = 9.013_801_955_9 * 10 ** -7
        a6 = 2.265_115_420_5 * 10 ** -8
        a7 = 3.607_115_659_3 * 10 ** -10
        a8 = 3.849_393_988_3 * 10 ** -12
        a9 = 2.821_352_192_5 * 10 ** -14
        a10 = 1.425_159_477_9 * 10 ** -16
        a11 = 4.876_866_228_6 * 10 ** -19
        a12 = 1.079_553_927_0 * 10 ** -21
        a13 = 1.394_502_706_2 * 10 ** -24
        a14 = 7.979_515_392_7 * 10 ** -28
        result =  sum([
            a0 * t ** 0,
            a1 * t ** 1,
            a2 * t ** 2,
            a3 * t ** 3,
            a4 * t ** 4,
            a5 * t ** 5,
            a6 * t ** 6,
            a7 * t ** 7,
            a8 * t ** 8,
            a9 * t ** 9,
            a10 * t ** 10,
            a11 * t ** 11,
            a12 * t ** 12,
            a13 * t ** 13,
            a14 * t ** 14,
        ]) / 1000
    elif 0 < t <= 400:
        a0 = 0.000_000_000_0 * 10 ** 0
        a1 = 3.874_810_636_4 * 10 ** 1
        a2 = 3.329_222_788_0 * 10 ** -2
        a3 = 2.061_824_340_4 * 10 ** -4
        a4 = -2.188_225_684_6 * 10 ** -6
        a5 = 1.099_688_092_8 * 10 ** -8
        a6 = -3.081_575_877_2 * 10 ** -11
        a7 = 4.547_913_529_0 * 10 ** -14
        a8 = -2.751_290_167_3 * 10 ** -17
        result =  sum([
            a0 * t ** 0,
            a1 * t ** 1,
            a2 * t ** 2,
            a3 * t ** 3,
            a4 * t ** 4,
            a5 * t ** 5,
            a6 * t ** 6,
            a7 * t ** 7,
            a8 * t ** 8,
        ]) / 1000
    return result - 0.011


def TC_E(t):
    '''TC/E 热电偶 温度转电动势 计算函数
    输入 ： t (摄氏度)
    输出 ： e (毫伏)
    '''
    if -270 <= t <= 0:
        a0 = 0.000_000_000_0 * 10 ** 0
        a1 = 5.866_550_870_8 * 10 ** 1
        a2 = 4.541_097_712_4 * 10 ** -2
        a3 = -7.799_804_868_6 * 10 ** -4
        a4 = -2.580_016_084_3 * 10 ** -5
        a5 = -5.945_258_305_7 * 10 ** -7
        a6 = -9.321_405_866_7 * 10 ** -9
        a7 = -1.028_760_553_4 * 10 ** -10
        a8 = -8.037_012_362_1 * 10 ** -13
        a9 = -4.397_949_739_1 * 10 ** -15
        a10 = -1.641_477_635_5 * 10 ** -17
        a11 = -3.967_361_951_6 * 10 ** -20
        a12 = -5.582_732_872_1 * 10 ** -23
        a13 = -3.465_784_201_3 * 10 ** -26
        return sum([
            a0 * t ** 0,
            a1 * t ** 1,
            a2 * t ** 2,
            a3 * t ** 3,
            a4 * t ** 4,
            a5 * t ** 5,
            a6 * t ** 6,
            a7 * t ** 7,
            a8 * t ** 8,
            a9 * t ** 9,
            a10 * t ** 10,
            a11 * t ** 11,
            a12 * t ** 12,
            a13 * t ** 13,
        ]) / 1000
    elif 0 < t <= 100:
        a0 = 0.000_000_000_0 * 10 ** 0
        a1 = 5.866_550_871_0 * 10 ** 1
        a2 = 4.503_227_558_2 * 10 ** -2
        a3 = 2.890_840_721_2 * 10 ** -5
        a4 = -3.305_689_665_2 * 10 ** -7
        a5 = 6.502_440_327_0 * 10 ** -10
        a6 = -1.919_749_550_4 * 10 ** -13
        a7 = -1.253_660_049_7 * 10 ** -15
        a8 = 2.148_921_756_9 * 10 ** -18
        a9 = -1.438_804_178_2 * 10 ** -21
        a10 = 3.596_089_948_1 * 10 ** -25
        return sum([
            a0 * t ** 0,
            a1 * t ** 1,
            a2 * t ** 2,
            a3 * t ** 3,
            a4 * t ** 4,
            a5 * t ** 5,
            a6 * t ** 6,
            a7 * t ** 7,
            a8 * t ** 8,
            a9 * t ** 9,
            a10 * t ** 10,
        ]) / 1000


def TC_K(t):
    '''TC/T 热电偶 温度转电动势 计算函数
    输入 ： t (摄氏度)
    输出 ： e (毫伏)
    '''
    if -270 <= t <= 0:
        a0 = 0.000_000_000_0 * 10 ** 0
        a1 = 3.945_012_802_5 * 10 ** 1
        a2 = 2.362_237_359_8 * 10 ** -2
        a3 = -3.285_890_678_4 * 10 ** -4
        a4 = -4.990_482_877_7 * 10 ** -6
        a5 = -6.750_905_917_3 * 10 ** -8
        a6 = -5.741_032_742_8 * 10 ** -10
        a7 = -3.108_887_289_4 * 10 ** -12
        a8 = -1.045_160_936_5 * 10 ** -14
        a9 = -1.988_926_687_8 * 10 ** -17
        a10 = -1.632_269_748_6 * 10 ** -20
        return sum([
            a0 * t ** 0,
            a1 * t ** 1,
            a2 * t ** 2,
            a3 * t ** 3,
            a4 * t ** 4,
            a5 * t ** 5,
            a6 * t ** 6,
            a7 * t ** 7,
            a8 * t ** 8,
            a9 * t ** 9,
            a10 * t ** 10,
        ]) / 1000
    elif 0 < t <= 1300:
        a0 = -1.760_041_368_6 * 10 ** 1
        a1 = 3.892_120_497_5 * 10 ** 1
        a2 = 1.855_877_003_2 * 10 ** -2
        a3 = -9.945_759_287_4 * 10 ** -5
        a4 = 3.184_094_571_9 * 10 ** -7
        a5 = -5.607_284_488_9 * 10 ** -10
        a6 = 5.607_505_905_9 * 10 ** -13
        a7 = -3.202_072_000_3 * 10 ** -16 # 
        a8 = 9.715_114_715_2 * 10 ** -20
        a9 = -1.210_472_127_5 * 10 ** -23
        c0 = 1.185_976 * 10 ** 2
        c1 = -1.183_432 * 10 ** -4
        # return (sum([
        #             a0 * t ** 0 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a1 * t ** 1 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a2 * t ** 2 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a3 * t ** 3 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a4 * t ** 4 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a5 * t ** 5 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a6 * t ** 6 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a7 * t ** 7 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a8 * t ** 8 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #             a9 * t ** 9 + c0 * math.exp(c1 * (t - 126.968_6) ** 2),
        #         ]) + a0) / 1000
        result = (((((((((a9 * t + a8) * t + a7) * t + a6) * t + a5) * t + a4) * t + a3) * t + a2) * t + a1) * t + a0) / 1000

        if 0 < t <= 19:
            result += 0.02
        elif 21 <= t <= 39 :
            result += 0.04
        elif 40 <= t <= 49 :
            result += 0.05
        elif 50 <= t <= 69 :
            result += 0.06
        elif 70 <= t <= 79 :
            result += 0.07
        elif 80 <= t <= 89 :
            result += 0.08
        elif 90 <= t <= 99 :
            result += 0.09
        elif 100 <= t <= 119 :
            result += 0.1
        elif 120 <= t <= 149 :
            result += 0.11
        elif 150 <= t <= 169 :
            result += 0.12
        elif 170 <= t <= 179 :
            result += 0.11
        elif 180 <= t <= 189 :
            result += 0.1
        elif 190 <= t <= 199 :
            result += 0.08
        elif 200 <= t <= 209 :
            result += 0.07
        elif 210 <= t <= 219 :
            result += 0.06
        elif 220 <= t <= 229 :
            result += 0.05
        elif 230 <= t <= 239 :
            result += 0.03
        elif 240 <= t <= 269 :
            result += 0.02
        elif 270 <= t <= 299 :
            result += 0.01
        return result

def average(lis):
    c = numpy.array(lis)
    return list(c.mean(axis=0))

def getRealAI(data):
    # self.set_current_value()
    data_ = []
    data_c = []
    # for xList in data:
        # xList = list(xList)
    vList = data
    # print(vList)
    # vList = [xList[0:8], xList[8:16], xList[16:24], xList[24:32]]
    # for value in zip(vList, sorted(self.AI_index)):
        # print(sorted(self.AI_index)[0:3])
        # print(value)
    for index, x in enumerate(vList):
        try:
            i = PointModel.get(PointModel.reg == 6, PointModel.channel == index + 1)
        # print(i)
            highValue = i.rhi
            lowValue = i.rlo
            z = (x * 1000 - 4) * (highValue - lowValue) / 16 + lowValue
            # print(z, x, x * 1000)
            data_c.append(z)
        except:
            data_c.append(x)
    # data_.append(data_c)
    # data_c = []
    # print(data_, 5555555)

    return data_c