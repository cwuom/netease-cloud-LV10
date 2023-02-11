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
[2]从歌曲中获取心动模式列表 / 推荐列表
[3]多线程将列表带入模拟播放器中
[4]刷完歌曲后待机一天
[5]新的一天开始，准时签到
=========================================

@im-cwuom - bilibili
"""


# 选取次数 [因为推荐的内容很多是已知的，当无法刷到300首时可以适当增加p值]
p = 25

# 记数器，不用管
x = 0

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
randomMax = 100
# 随机的最小数值 不要超过上面的变量就可以
randomMin = 0

"""
1 -> 当模式0无法使用时(无法稳定增加听歌量),使用播放1 可能对推荐算法有一定影响（刷官方推荐的歌单）
0 -> 根据心动模式来进行刷听歌量 对推荐算法影响微乎其微
"""
PlayMode = 0 # 播放模式 


"""刷播放函数 心动模式"""
def startPlay(data):
    global x
    tlist = []
    for id in data:
        id = id["id"]
        t1 = Thread(target=Play, args=(id,))
        t1.start()
        tlist.append(t1)
    
    for t in tlist:
        t.join()


"""刷播放函数 若上一个用不了，请尝试这个(对推荐算法可能会产生影响)"""
def startPlay2():
    try:
        sidList = []

        source_ids = json.loads(requests.get("http://localhost:3000/recommend/resource", cookies=cookies, headers=headers).text)
        for ids in source_ids["recommend"]:
            id = ids["id"]
            sidList.append(id)
            print("推荐歌单->",id,"已加入播放列表!")


        musicIdsList = []
        for ids in sidList:
            # /playlist/track/all?id=24381616
            musicList = json.loads(requests.get("http://localhost:3000/playlist/track/all?id="+str(ids), cookies=cookies, headers=headers).text)
            for id in musicList["privileges"]:
                print("获取到音乐:",id["id"])
                musicIdsList.append(id["id"])

        print("总歌曲数量:",len(musicIdsList), "开始播放(mode2)")
        global x
        tlist = []
        for id in musicIdsList:
            t1 = Thread(target=Play, args=(id,))
            t1.start()
            tlist.append(t1)

        for t in tlist:
            t.join()
            
    except:
        print("抱歉, 您的账号不兼容与PlayMode=1(也许是因为听歌太少了?), 请尝试PlayMode=0")
cookies={}
f = open("cookie.txt", "r")


"""模拟播放函数 便于多线程(火力全开)"""
def Play(id):
    global x
    id = id
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


for line in f.read().split(';'):
    name,value=line.strip().split('=',1)
    cookies[name]=value  #为字典cookies添加内容

headers = {'content-type': "application/json", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}
# 488249475

# [api]/playmode/intelligence/list?id=1381290206&pid=3031717021
# [api]/likelist [ids]


while True:
    if PlayMode == 0:
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
    elif PlayMode == 1:
        startPlay2()
    else:
        print("[ERR] 请检查您的PlayMode =",PlayMode,"是否正确!")
        time.sleep(10)
        exit()
    print("本次任务已完成!")
    x = 0
    for y in range(86400):
        time.sleep(1)
        print("下次运行:",86400-y)
