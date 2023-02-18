# 3031717021
import requests
import time
from threading import Thread
import json
import random

"""
仅供娱乐 打压pdd上面拿这个卖钱的
"""


succeed = 0
failed = 0

def main():
    global succeed
    global failed
    cookies = {}
    f = open("cookie.txt", "r")
    for line in f.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value

    headers = {'content-type': "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"}

    while True:
        t1 = Thread(target=play, args=(headers, cookies))
        t1.start()
        print("\rsucceed =", succeed, "| failed =", failed, end="", flush=True)


def play(headers, cookies):
    try:
        global succeed
        global failed
        sourceid = "1849703902"  # 歌单ID
        play_time = "123"  # 播放时间
        musicid = "1381290206"  # 歌曲ID

        t = time.time()
        t = str(int(round(t * 1000)))
        res = requests.get(
            "http://127.0.0.1:3000/scrobble?id=" + musicid + "&sourceid=" + sourceid + "&time=" + play_time + "&timestamp=" + t,
            cookies=cookies, headers=headers)

        if res.text == """{"code":200,"data":"success","message":""}""":
            succeed += 1
        else:
            failed += 1

        t1 = Thread(target=play, args=(headers, cookies))
        t1.start()


    except:
        pass



if __name__ == '__main__':
    main()
