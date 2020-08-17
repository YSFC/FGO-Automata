from core.Automata import Automata
import logging
import time
import uiautomator2 as u2
import os


def connect():  # 连接adb与uiautomator
    try:
        # os.system 函数正常情况下返回是进程退出码，0为正常退出码，其余为异常
        # 雷电模拟器
        if os.system('cd adb && adb connect 127.0.0.1:5554') != 0:
            print("连接模拟器失败")
            exit(1)
        # os.system('cd adb & adb connect 127.0.0.1:7555') #mumu模拟器
        if os.system('python -m uiautomator2 init') != 0:
            print("初始化 uiautomator2 失败")
            exit(1)
    except Exception as e:
        print('连接失败, 原因: {}'.format(e))
        exit(1)

    result = os.popen('adb devices')  # 返回adb devices列表
    res = result.read()
    lines = res.splitlines()[0:]
    while lines[0] != 'List of devices attached ':
        del lines[0]
    del lines[0]  # 删除表头

    device_dic = {}  # 存储设备状态
    for i in range(0, len(lines) - 1):
        lines[i], device_dic[lines[i]] = lines[i].split('\t')[0:]
    lines = lines[0:-1]
    for i in range(len(lines)):
        if device_dic[lines[i]] != 'device':
            del lines[i]
    print(lines)
    return lines


devices = connect()
if len(devices) == 0:
    exit("模拟器未启动或其它错误")
    
#logging.basicConfig(filename='automata.log',filemode='w',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',datefmt='%y/%m/%d %I:%M:%S %p') 


bb = Automata("assets/Ember4.png", "assets/wucan.png", (0, 0),u2ConnectUrl = devices[0])
bb.set_apples(10, "assets/gold.png")

count = 0
while count < 27:
    bb.quick_start()
    time.sleep(10)
    # BATTLE 1
    bb.select_servant_skill(2, mode = 1)
    bb.select_servant_skill(4)
    bb.select_servant_skill(5)
    #bb.select_servant_skill(7)
    #bb.select_servant_skill(9)
    bb.select_servant_skill(9)
    bb.select_cards([8])
    time.sleep(15)

    # BATTLE 2
    bb.select_servant_skill(3)
    bb.select_cards([6])
    time.sleep(18)

    # BATTLE 3
    bb.select_cards([7])
    time.sleep(10)
    # FINISH
    bb.finish_battle()
    time.sleep(5)

