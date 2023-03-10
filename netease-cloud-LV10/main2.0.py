"""
网易云一键LV10

[python 3.7.9]

* main2.0 测试较少，但功能相对增多，可自定义性提升，优化部分代码，若出现致命BUG请使用main.py *

=====================================
如何工作?->
[1]从喜欢列表随机挑选部分歌曲
[2]从歌曲中获取心动模式列表 / 推荐列表
[3]多线程将列表带入模拟播放器中
[4]刷完歌曲后待机一天
[5]新的一天开始，准时签到
=========================================

@im-cwuom - bilibili
       请关注我

注: 按下回车终止所有线程
"""



# ==============================================配置==============================================

"""
此项为你的网易云UID 如果值为auto则会自动获取UID
若程序无法自动获取您的UID，请删除"auto"并手动填写此项


* 如何获取?
> http://localhost:3000/qrlogin.html 中找到"id": xxxxx(xxx为纯数字)后复制 替换下面的UID 
        http://localhost:3000/因需求改变，取决与你的服务器搭建在何处，若在此电脑上搭建请直接访问它
"""
UID = "auto"


# 选取次数 [因为推荐的内容很多是已知的，当无法刷到300首时可以适当增加p值]
p = 25

# 你的API接口 [最后不要加斜杠] eg http://127.0.0.1:3000
api = "http://localhost:3000"
# 你的歌单ID(喜欢列表)
sourceid = "1849703902"

"""
是否听完全曲 
True -> 听完全曲(会多一份请求，可能对效率有影响) 
False -> 听完部分(本地计算随机数, 60s以上算入听歌量)
"""
ListenAll = False

# 看你的歌单中的音乐有多少 设定数量不要少于[p + randomMax] 否则可能会报错(下标越界)
randomMax = 50
# 随机的最小数值 不要超过上面的变量就可以
randomMin = 0

"""
1 -> 当模式0无法使用时(无法稳定增加听歌量),使用播放1 可能对推荐算法有一定影响（刷官方推荐的歌单）
0 -> 根据心动模式来进行刷听歌量 对推荐算法影响微乎其微

*当启用MaxContinueNum时，也许会自动改变此数值来达到期望听歌量*
"""
PlayMode = 1  # 播放模式

"""
最大尝试次数
当每日播放未达到期望值时，重启程序并尝试达到期望听歌量

0 -> 关闭
1 -> 尝试1次后休眠
n -> 尝试n次后休眠
.....

-1 -> 一直尝试，直到达到期望值（慎用）
"""
MaxContinueNum = 2

"""
刷到300首后停止
会多一份请求，默认开启
"""
Enable300 = True

# 没有部分多线程的日志(还是有日志) 可以认真查看已经刷了多少听歌量了
NoThreadLogs = True

# 期望值，若达不到期望值则会推倒重来
ExpectationNum = 250


"""
给网易云喘息的机会，不然容易风控，如果你觉得影响效率可适当降低此数值
(主要原因是多线程吃带宽太快了，会影响听歌量的获取，若你没有开启Enable300则可以忽视)
"""
if Enable300:
    # 你应该调整这里
    SleepTime = 1.3
else:
    SleepTime = 0.1

# 忽略UID解析错误提示，将在提示过后自动变为True
IgnoreUidError = False


# ==============================================================================================

import sys
from threading import Thread
import time
import json
import random


import ctypes
import inspect
import requests
import keyboard

"""
使用前请先安装上面的库
=====================================
管理员运行CMD
> pip3 install 缺失的库名(import后面) -i https://pypi.tuna.tsinghua.edu.cn/simple
"""


# 记数器，不用管
x = 0
# 不用管，判断是否300首
Already300 = False
# 终止播放判断，不用管
StopPlay = False
PlayingMusicId = -1

# UID
uid = 0

# 记录听歌量
s = 0

# 储存所有线程
ThreadList = []

# 已经进入休眠
OnSleep = False

ListenerThread = []


while True:
    try:
        cookies = {}
        f = open("cookie.txt", "r")

        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value  # 为字典cookies添加内容

        break
    except:
        cookie = input(
            "未检测到cookie.txt中含有指定cookie，或是文件不存在? \n请输入有效的网易云cookie!\n=========================\n[cookie]")
        print("\n=========================")
        with open("cookie.txt", "w") as w:
            w.write(cookie)

headers = {'content-type': "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}

"""刷播放函数 心动模式"""


def startPlay(data):
    global ThreadList
    global SleepTime
    try:
        tlist = []
        # print(data)
        for id in data:
            if not Already300:
                id = id["id"]
                t1 = Thread(target=Play, args=(id,))
                t1.start()
                time.sleep(SleepTime)
                tlist.append(t1)
                ThreadList.append(t1)

        for t in tlist:
            t.join()
    except:
        print("\n[ERR] 播放模式出现问题，可能会影响使用，您可能被网易云风控了")


"""刷播放函数 若上一个用不了，请尝试这个(对推荐算法可能会产生影响)"""


def startPlay2():
    global SleepTime
    global Already300
    global ThreadList
    global NoThreadLogs
    try:
        sidList = []

        if not Already300:
            source_ids = json.loads(requests.get(api + "/recommend/resource", cookies=cookies, headers=headers).text)
            for ids in source_ids["recommend"]:
                id = ids["id"]
                sidList.append(id)
                log_print("推荐歌单->", id, "已加入播放列表!")

            musicIdsList = []
            for ids in sidList:
                # /playlist/track/all?id=24381616
                try:
                    musicList = json.loads(
                        requests.get(api + "/playlist/track/all?id=" + str(ids), cookies=cookies, headers=headers).text)
                    for id in musicList["privileges"]:
                        log_print("获取到音乐:", id["id"])
                        musicIdsList.append(id["id"])
                except:
                    print("\n[ERR] 忽略了一个歌单数据 : 无法解析")

        print("\n总歌曲数量:", len(musicIdsList), "开始播放(mode2)")
        global x
        tlist = []
        for id in musicIdsList:
            if not Already300:
                t1 = Thread(target=Play, args=(id,))
                t1.start()
                tlist.append(t1)
                ThreadList.append(t1)
                time.sleep(0.1)

        for t in tlist:
            t.join()

    except Exception as e:
        print("\n抱歉, 您的账号不兼容与PlayMode=1(也许是因为听歌太少了?), 请尝试PlayMode=0\nerr>",e)


"""
重写print，用于判断是否打印不重要的日志
"""


def log_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    if not NoThreadLogs:
        print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)


"""模拟播放函数 便于多线程(火力全开)"""


def Play(id):
    global ThreadList
    global x
    global Already300
    global MaxContinueNum
    global uid
    global s
    global StopPlay
    global PlayingMusicId
    if not Already300:
        try:
            PlayingMusicId = id
            x += 1
            t = time.time()
            t = str(int(round(t * 1000)))
            if not ListenAll:
                playTime = random.randint(90, 120)
                a = requests.get(
                    api + "/scrobble?id=" + str(id) + "&sourceid=" + sourceid + "&time=" + str(
                        playTime) + "&timestamp=" + t,
                    cookies=cookies, headers=headers)
                log_print(a.text)
                log_print("ID->" + str(id) + " -- OK!")
                log_print("x->" + str(x))
            else:
                a = requests.get(api + "/song/detail?ids=" + str(id), cookies=cookies, headers=headers)
                dt = json.loads(a.text)
                dt = dt["songs"]
                dt = dt[0]["dt"]
                dt = str(dt)[0:3]
                log_print("歌曲时间(s)->", dt)
                playTime = random.randint(90, 120)
                a = requests.get(
                    api + "/scrobble?id=" + str(id) + "&sourceid=" + sourceid + "&time=" + str(dt) + "&timestamp=" + t,
                    cookies=cookies, headers=headers)
                log_print(a.text)
                log_print("ID->" + str(id) + " -- OK!")
                log_print("x->" + str(x))

            time.sleep(0.3)
        except:
            pass
    else:
        # print("300! Stop")
        exit()
        StopPlay = True


def SongsListener():
    global ThreadList
    global s
    global uid
    global Already300
    s1 = GetListenSongs(uid)
    while True:
        if not OnSleep:
            try:
                global Already300
                # print("当前听歌量: ", s1)
                if not StopPlay:
                    s2 = GetListenSongs(uid)
                    s = s2 - s1
                    # s = 300
                    if s >= 300:
                        Already300 = True
                        time.sleep(1)
                        print("\r[STOP] 已到达300首，所有请求已被关闭，等待剩余线程自动终止后进入休眠(x=" + str(x) + ")",
                              end="", flush=True)
                        break
                else:
                    break

            except:
                continue

        else:
            break


def ShowLogs():
    global x
    global s
    global PlayingMusicId
    n = 0
    while True:
        if OnSleep or Already300:
            break
        if PlayingMusicId != -1:
            print("\r听歌量 =", s, "| 听歌数 = ", x, "| ID =", PlayingMusicId,"        ", end="", flush=True)
        else:
            print("\r[STARTING] 正在获取数据并解析，请稍后", "." * (n % 4), "     " , end="", flush=True)
            n += 1

        time.sleep(0.3)


"""获取听歌量"""


def GetListenSongs(uid):
    global ThreadList
    for x in range(100):
        try:
            t = time.time()
            t = str(int(round(t * 1000)))
            # http://localhost:3000/login/status
            a = requests.get(api + "/user/detail?uid=" + str(uid) + "&timestamp=" + t, cookies=cookies, headers=headers)
            listenSongs = json.loads(a.text)
            listenSongs = listenSongs["listenSongs"]
            # print("累积听歌->", listenSongs)
            return listenSongs
        except:
            continue


"""开始"""


def start():
    global ThreadList
    global Already300
    global MaxContinueNum
    global x
    global StopPlay
    global uid
    global ExpectationNum
    global s
    global PlayMode
    global UID
    global IgnoreUidError
    global OnSleep
    global ListenerThread

    if not OnSleep:
        if UID == "auto":
            try:
                print("\n=================================")
                print("[Connecting] "+api)
                t = time.time()
                t = str(int(round(t * 1000)))
                res = requests.get(api + "/login/status?" + "&timestamp=" + t, cookies=cookies, headers=headers)
                # print(res.text)
            except:
                print("[ERR] 此程序未能连接到您的API! 请检查您的API是否已经跑起来了?")
                sys.exit()
            uid = json.loads(res.text)
            # print(res.text)
            print("[Connected] " + api+"\n=================================\n")
            while True:
                try:
                    uid = uid["data"]["profile"]["userId"]
                except:
                    if not IgnoreUidError:
                        print("[ERR] 未能正确获取到UID，正在尝试更换解析方式")
                    res = requests.get(api + "/login/status?" + "&timestamp=" + t, cookies=cookies, headers=headers)
                    uid = json.loads(res.text)
                    try:
                        uid = uid["data"]["account"]["id"]
                        IgnoreUidError = True
                        break
                    except:
                        print("[ERR] 无法解析UID，请尝试更改源码顶部中的UID选项")
                        sys.exit(-1)
                    time.sleep(5)
                    continue

        else:
            uid = UID

        print("用户UID:", uid)
        try:
            nickname = requests.get(api + "/user/detail?uid=" + str(uid) + "&timestamp=" + t, cookies=cookies, headers=headers)
            nickname = json.loads(nickname.text)
            nickname = nickname["profile"]["nickname"]
        except:
            print("[ERR] 在处理UID="+str(uid)+"时发生错误(未能解析到nickname)，请确认UID正确！")
            exit(-1)

        print("用户昵称:", nickname)

        if Enable300:
            t1 = Thread(target=SongsListener, args=())
            t1.start()
            ThreadList.append(t1)

            t2 = Thread(target=ShowLogs, args=())
            t2.start()
            ThreadList.append(t1)
            ThreadList.append(t2)

        if PlayMode == 0:
            res2 = requests.get(api + "/likelist", cookies=cookies, headers=headers)

            log_print(res2.text)
            data_ids = json.loads(res2.text)
            data_ids = data_ids["ids"]

            # 这里从喜欢列表提取几个ID 进行心动模式刷歌曲
            idsList = []
            for i in range(p):
                r = random.randint(randomMin, randomMax)
                idsList.append(data_ids[i + r])

            res = requests.get(api + "/daily_signin", cookies=cookies, headers=headers)  # 签到
            log_print("签到成功! -> " + res.text)

            tlist = []
            print("\n选取次数:", p, "开始播放(mode1)")
            for n in range(p):
                try:
                    t = time.time()
                    t = str(int(round(t * 1000)))
                    a1 = requests.get(
                        api + "/playmode/intelligence/list?id=" + str(
                            idsList[n]) + "&pid=" + sourceid + "&timestamp=" + t,
                        cookies=cookies, headers=headers)
                    data = json.loads(a1.text)
                    data = data["data"]
                    time.sleep(0.1)
                    # log_print(data)
                    t1 = Thread(target=startPlay, args=(data,))
                    t1.start()
                    tlist.append(t1)
                    ThreadList.append(t1)
                except:
                    print("[ERR] 数据获取失败，正在重新请求并解析数据")
                    continue

            for ts in tlist:
                ts.join()
        elif PlayMode == 1:
            startPlay2()
        else:
            log_print("\n[ERR] 请检查您的PlayMode =", PlayMode, "是否正确!")
            time.sleep(10)
            exit()
        print("\n本次任务已完成!")

        if s <= ExpectationNum:
            if MaxContinueNum != -1:
                if MaxContinueNum > 0:
                    if (MaxContinueNum - 1) <= 0:
                        PlayMode = 1
                    else:
                        PlayMode = 0
                    MaxContinueNum -= 1

                    print("\n未达到期望值，正在重试")
                    start()
        elif MaxContinueNum == -1:
            start()

    # Already300 = False
    # StopPlay = False
    # s = 0
    # x = 0


"""线程杀手"""


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# 488249475

# [api]/playmode/intelligence/list?id=1381290206&pid=3031717021
# [api]/likelist [ids]

def StopAllThread():
    global OnSleep
    global Already300
    while not OnSleep:
        for t in ThreadList:
            try:
                stop_thread(t)
                print("\r[STOPPING] 正在终止进程 >", t, end="", flush=True)
                Already300 = True
                OnSleep = True
            except:
                pass
    print("\n[KILL] OK")


def StopListener():
    global OnSleep
    global Already300
    while True:
        if OnSleep:
            break
        try:
            keyboard.wait("`")
        except:
            print("\n[STOP] 监听线程异常退出，请再次终止运行来关闭此程序")
        StopAllThread()


if __name__ == '__main__':
    while True:
        Already300 = False
        StopPlay = False
        x = 0
        s = 0
        ThreadList = []
        OnSleep = False

        t1 = Thread(target=StopListener, args=())
        t1.start()
        ListenerThread.append(t1)

        start()

        OnSleep = True
        now_hour = time.strftime("%H", time.localtime())
        now_min = time.strftime("%M", time.localtime())
        if now_hour < "08":
            rest = 8 - int(now_hour)
            sleeptime = (rest - 1) * 3600 + (60 - int(now_min)) * 60
        elif now_hour > "08":
            rest = 8 - int(now_hour) + 24
            sleeptime = (rest - 1) * 3600 + (60 - int(now_min)) * 60
        elif now_hour == "08":
            continue

        sleeptime = sleeptime + 3600
        for y in range(sleeptime):
            time.sleep(1)
            print("\r[Waitting] 下次运行:", sleeptime - y, "   ", end="", flush=True)
