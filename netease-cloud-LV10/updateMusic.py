# 3031717021
import requests
import time
from threading import Thread
import json
import random

"""
仅供娱乐 效率可能不怎么样
"""


sourceid = "1849703902" # 歌单ID
play_time = "123" # 播放时间
musicid = "22504151" # 歌曲ID

def main():
    global x
    cookies={}
    f = open("cookie.txt", "r")
    for line in f.read().split(';'):
        name,value=line.strip().split('=',1)
        cookies[name]=value  #为字典cookies添加内容

    headers = {'content-type': "application/json", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}

    while True:
        t = time.time()
        t = str(int(round(t * 1000)))
        a = requests.get("http://127.0.0.1:3000/scrobble?id="+musicid+"&sourceid="+sourceid+"&time="+play_time+"&timestamp="+t, cookies=cookies, headers=headers)
        print("刷了",x,"次")
        x += 1


for x in range(100): # 100个线程并发
    t1 = Thread(target=main)
    t1.start()
    time.sleep(1)