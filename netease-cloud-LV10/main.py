import requests
import time
from threading import Thread
import json
import random
import os

"""
网易云一键LV10

[python 3.7.9]

=====================================
如何工作?-> 
[1]从喜欢列表随机挑选部分歌曲
[2]从歌曲中获取心动模式列表
[3]多线程将列表带入模拟播放器中
[4]刷完歌曲后待机一天
[5]新的一天开始，准时签到
=========================================

@im-cwuom - bilibili
"""


# 选取次数
p = 10

# 记数器，不用管
x = 0

# 你的API接口 [最后不要加斜杠] eg http://127.0.0.1:3000
api = "http://localhost:3000"
# 你的歌单ID(喜欢列表)
sourceid = "1849703902"


ListenAll = True

# 看你的歌单中的音乐有多少 设定数量不要少于[p + randomMax] 否则可能会报错(下标越界)
randomMax = 100
# 随机的最小数值 不要超过上面的变量就可以
randomMin = 0

"""刷播放函数 心动模式"""
def startPlay(data):
    global x
    for id in data:
        id = id["id"]
        x += 1
        t = time.time()
        t = str(int(round(t * 1000)))
        if not ListenAll:
            playTime = random.randint(90, 120)
            a = requests.get(api+"/scrobble?id="+str(id)+"&sourceid="+sourceid+"&time="+str(playTime)+"&timestamp="+t, cookies=cookies, headers=headers)
            print(a.text)
            print("ID->" + str(id) + " -- OK!")
            print("x->" + str(x))
            time.sleep(0.3)
        else:
            a = requests.get(api+"/song/detail?ids="+str(id), cookies=cookies, headers=headers)
            dt = json.loads(a.text)
            dt = dt["songs"]
            dt = dt[0]["dt"]
            dt = str(dt)[0:3]
            print("歌曲时间(s)->",dt)
            playTime = random.randint(90, 120)
            a = requests.get(api+"/scrobble?id="+str(id)+"&sourceid="+sourceid+"&time="+str(dt)+"&timestamp="+t, cookies=cookies, headers=headers)
            print(a.text)
            print("ID->" + str(id) + " -- OK!")
            print("x->" + str(x))
            time.sleep(0.3)


cookies={}
f = open("cookie.txt", "r")

for line in f.read().split(';'):
    name,value=line.strip().split('=',1)
    cookies[name]=value  #为字典cookies添加内容

headers = {'content-type': "application/json", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}
# 488249475

# [api]/playmode/intelligence/list?id=1381290206&pid=3031717021
# [api]/likelist [ids]


while True:
    a2 = requests.get(api+"/likelist", cookies=cookies, headers=headers)

    print(a2.text)
    data_ids = json.loads(a2.text)
    data_ids = data_ids["ids"]

    # 这里从喜欢列表提取几个ID 进行心动模式刷歌曲
    idsList = []
    for i in range(p):
        r = random.randint(randomMin, randomMax)
        idsList.append(data_ids[i + r])


    t = time.time()
    t = str(int(round(t * 1000)))
    a = requests.get(api+"/daily_signin", cookies=cookies, headers=headers) # 签到
    print("签到成功! -> "+a.text)


    tlist = []
    for n in range(p):
        t = time.time()
        t = str(int(round(t * 1000)))
        a1 = requests.get(api+"/playmode/intelligence/list?id="+str(idsList[n])+"&pid="+sourceid+"&timestamp="+t, cookies=cookies, headers=headers)
        data = json.loads(a1.text)
        data = data["data"]
        time.sleep(0.1)
        # print(data)
        t1 = Thread(target=startPlay, args=(data,))
        t1.start()
        tlist.append(t1)


    for ts in tlist:
        ts.join()
    print("本次任务已完成!")
    for y in range(86400):
        time.sleep(1)
        print("下次运行:",86400-y)
    

