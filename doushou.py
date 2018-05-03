# -*- coding: utf-8 -*-
import os
import shutil
import datetime,time
import math
import random
import json
from PIL import Image, ImageDraw
import wda
from PIL import Image
import colorsys
import pytesseract
import datetime
import pygame
import sqlite3
from subprocess import call
c = wda.Client()
s = c.session()
conn = sqlite3.connect('test.db')
cur = conn.cursor()

def pull_screenshot(name):
    c.screenshot(name)

def jumps(x,y):
    s.tap(x, y)
# def text():
#     # -*- coding: UTF-8 -*-
#
#     from aip import AipOcr
#     import json
#
#     # 定义常量
#     APP_ID = '9851066'
#     API_KEY = 'LUGBatgyRGoerR9FZbV4SQYk'
#     SECRET_KEY = 'fB2MNz1c2UHLTximFlC4laXPg7CVfyjV'
#
#     # 初始化AipFace对象
#     aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
#     # 读取图片
#     filePath = "1.png"
#
#     def get_file_content(filePath):
#         with open(filePath, 'rb') as fp:
#             return fp.read()
#
#             # 定义参数变量
#
#     options = {
#         'detect_direction': 'true',
#         'language_type': 'ENG',
#     }
#
#     # 调用通用文字识别接口
#     result = aipOcr.basicGeneral(get_file_content(filePath), options)
#     print(json.dumps(result).decode("unicode-escape"))
area = {
    'home':(935,1848,1003,1936),
    'pk': (232, 826, 321, 1159),
    'pk2': (322, 1412, 392, 1648),
    'money': (370, 1693, 443, 1732),
    'getMoney': (370, 1693, 443, 1732),
    'auto': (101, 1876, 125, 1959),
    'refresh': (334, 1162, 403, 1332),
    'refresh2': (678, 661, 780, 748),
    'done': (102, 998, 192, 1259),
    'levUp': (48, 890, 105, 1107),
    'des': (58, 1714, 108, 1768),
}
mainColor = {
    'home':((139, 0, 0)),#首页主要颜色
    'pk': (61, 216, 104),
    'pk2': (249, 200, 0),
    'money': (194, 166, 93),
    'getMoney': (194, 166, 93),
    'auto': (221, 221, 221),
    'done': (61, 216, 104),
    'levUp': (58, 137, 214),
    'refresh': (58, 214, 104),
    'refresh2': (255, 223, 185),
    'des':(92, 151, 255)
}
tap = {
    'home':[960, 1860],#首页按钮
    'pk': [255, 970],#开始战斗
    'pk2': [579, 1599],#开始战斗
    'money': [420, 1695],#金币
    'getMoney': [375, 980],#领取金币
    'auto': [93, 1920],#自动战斗
    'refresh': [360,1236],#网络重连
    'done': [150, 1100],#
    'levUp': [78, 1071],#升阶按钮
    'des': [84, 1738],#防御按钮
}

def pil(box):
    im = Image.open('1.png')
    region = im.crop(box)
    # region.show()
    return get_dominant_color(region)

def get_dominant_color(image):
    image = image.convert('RGBA')
    image.thumbnail((100, 100))
    max_score = 0
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color

def errorE(flag):
    while flag!='nn':
        if (oper('home')):
            n=0
            s.tap(tap['home'][0], tap['home'][1])
            while not (oper('pk') or oper('auto')):
                if oper('pk2'):
                    s.tap(tap['pk2'][0], tap['pk2'][1])
                    flag='nn'
                    break
                else:
                    if n <5:
                        time.sleep(10)
                        print(u'线程挂起10秒，等待重连。。。')
                        n+=1
                    else:
                        warning()
                        break
            if (oper('pk')):
                s.tap(tap['pk'][0], tap['pk'][1])
                print(u'异常处理完成，重新战斗。。。')
                break
            elif (oper('auto')):
                s.tap(tap['auto'][0], tap['auto'][1])
                print(u'异常处理完成，重新自动战斗。。。')
                break
        elif (oper('refresh2')):
            s.tap(tap['refresh'][0], tap['refresh'][1])
            break




def oper(obj):
    pull_screenshot('1.png')
    col = pil(area[obj])
    flag = False
    if(col == mainColor[obj]):
        flag = True
    return flag


pygame.mixer.init()
def getNewDay(midnight):
    data = {}
    cursor = cur.execute("SELECT fight,money from lyx where times=%s"%(midnight))
    querys = cursor.fetchall()
    if not querys:
       cur.execute("INSERT INTO lyx (times,money,fight) VALUES (%s,0, 0)"%(midnight))
       print(u'新的一天开始了')
       conn.commit()
    else:
        for q in querys:
            data['count']=q[0]
            data['money']=q[1]
        return data
def warning():
    # file = r'1.mp3'
    # pygame.mixer.init()
    # print(u"程序异常，播放提示音。。。")
    # track = pygame.mixer.music.load(file)
    # pygame.mixer.music.play()
    # time.sleep(215)
    # pygame.mixer.music.stop()
    # print(u'程序终止，进程关闭')
    # exit(0)

    cmd = 'display notification \"' + \
          "程序异常了！！！" + '\" with title \"程序异常通知\"'
    call(["osascript", "-e", cmd])
    exit(0)

def main():
    now = time.time()
    midnight = int((now - (now % 86400) + time.timezone) * 1000)
    d = getNewDay(midnight)
    count = 0
    money = 0
    if d:
        count = d['count']
        money = d['money']
    ss = 0
    while ss == 0:
        getNewDay(midnight)
        ss += 1
        qq = 0
        nn = 0
        if(oper('pk')):
            ss = 0
            s.tap(tap['pk'][0], tap['pk'][1])
            print (u'点击战斗按钮。。。')
            sTime = datetime.datetime.now()
            time.sleep(15)
            num = 1
            while not oper('auto'):
                qq += 1
                print (u'动画进行中，未到战斗界面，线程挂起4秒等待。。。')
                time.sleep(4)
                if qq > 8:
                    # errorE(True)
                    warning()
            # if not d:
            s.tap(tap['auto'][0], tap['auto'][1])
            print (u'自动战斗开始。。。')
            while not oper('done'):
                # if d:
                    # mac=0
                    # while oper('des'):
                    #     s.tap(tap['des'][0],tap['des'][1])
                    #     print(u'点击防御按钮，线程挂起5秒等待')
                    #     time.sleep(5)
                # else:
                nn += 1
                tm = 60 / num
                print (u'战斗进行中，线程挂起%s秒等待，重新检测状态。。。'% tm)
                time.sleep(tm)
                if (num < 5):
                    num += 2
                else:
                    num = 5

                if(nn > 15):
                    # errorE(True)
                    warning()
                if (oper('refresh2')):
                    s.tap(tap['refresh'][0], tap['refresh'][1])
            s.tap(tap['done'][0], tap['done'][1])
            count += 1
            eTime = datetime.datetime.now()
            times = (eTime-sTime).seconds
            cur.execute("UPDATE lyx set fight = %d where times=%s" % (count, midnight))
            conn.commit()
            print(time.strftime("%H:%M:%S")+u' 战斗结束，战斗时长%s秒，战斗次数统计+1，当前共战斗%s次，返回初始界面。。。' %(times, count))
            time.sleep(2)
            if(oper('levUp')):
                s.tap(tap['levUp'][0], tap['levUp'][1])
                print(u'恭喜你升阶了，关闭升阶界面')
                time.sleep(2)
            if(oper('money')):
                s.tap(tap['money'][0], tap['money'][1])
                s.tap(tap['getMoney'][0], tap['getMoney'][1])
                money += 1
                cur.execute("UPDATE lyx set money = %d where times=%s"% (money, midnight))
                conn.commit()
                print(u'领取金币，当前共领取金币%s次。。。' % money)
                time.sleep(2)
        # else:
        #     errorE(True)
        #     ss=0
        print(u'***************************战斗循环***************************')
    warning()

def a(aq):
    while aq:
        if aq==1:
            print(1111)
            break
        else:
            print(2222)
            break
if __name__ == '__main__':
    main()
    # pull_screenshot('1.png')

    # print (pil(area['levUp']))