# **NeteaseCloudMusicTools**   - 网易云升级助手

####bilibili - im-cwuom 关注我获取更多!

------------



### :fa-question-circle: 关于NeteaseCloudMusicTools
#### 功能方面 :fa-cog:
- 每天(9点)稳定300首 + 自动签到
- 刷单曲听歌量，效率极高
- 丰富的自定义性，可根据自己的升级需求来更改单独配置
- 刷到300首自动终止, 不占用多余带宽, 当听歌量无法满足时可以卷土重来
- 自动启用api服务
- ...
------------
#### 登录方面 :fa-qrcode:
- 支持qrlogin(扫码登录)自动获取cookie
- 支持调起多种主流浏览器(Chrome/Firefox/Edge/Safari)
- 当cookie失效时自动重新要求登录
------------
#### 效率方面 :fa-paper-plane:
- 所有方案基本都采用多线程，不用担心效率低下

------------

#### 支持的平台 :fa-check:
- 打包版本目前只支持windows，但源码可以复制到linux主机上(前提: 有py环境, 模块正常)

------------

#### 便携性/兼容性 :fa-thumbs-o-up:
- 操作简单，哪怕没有基础也可以快速部署，因为看见有人收费所以想着自己做了一个，但网上大多数升级工具(除收费，网站版)部署困难，但此程序已经整合了所需环境，双击打开就可运行
- 不兼容Windows 7或老架构的机器，测试环境Windows 11 专业版 22H2


------------

### 脚本截图
[![s1](https://raw.githubusercontent.com/cwuom/netease-cloud-LV10/main/s1.png "s1")](https://raw.githubusercontent.com/cwuom/netease-cloud-LV10/main/s1.png "s1")


------------

### config.ini

[setting]
;你的API接口 [最后不要加斜杠] eg http://127.0.0.1:3000
api = http://localhost:3000

;选取次数 [因为推荐的内容很多是已知的，当无法刷到300首时可以适当增加p值]
p = 25

;你的歌单ID(喜欢列表)
SourceID = 2706514248



;此项为你的网易云UID 如果值为auto则会自动获取UID
;若程序无法自动获取您的UID，请删除auto并手动填写此项

;* 如何获取?
;> http://localhost:3000/qrlogin.html 中找到id: xxxxx(xxx为纯数字)后复制 替换下面的UID
;http://localhost:3000/因需求改变，取决与你的服务器搭建在何处，若在此电脑上搭建请直接访问它
UID = auto




;播放模式
;1 -> 当模式0无法使用时(无法稳定增加听歌量),使用播放1 可能对推荐算法有一定影响（刷官方推荐的歌单）
;0 -> 根据心动模式来进行刷听歌量 对推荐算法影响微乎其微

;*当启用MaxContinueNum时，也许会自动改变此数值来达到期望听歌量*
PlayMode = 1



;是否听完全曲
;True -> 听完全曲(会多一份请求，可能对效率有影响)
;False -> 听完部分(本地计算随机数, 60s以上算入听歌量)
ListenAll = True

;看你的歌单中的音乐有多少 设定数量不要少于[p + randomMax] 否则可能会报错(下标越界)
randomMax = 50
;随机的最小数值 不要超过上面的变量就可以
randomMin = 0

;===================================================
;最大尝试次数
;当每日播放未达到期望值时，重启程序并尝试达到期望听歌量
;===================================================
;0 -> 关闭
;1 -> 尝试1次后休眠
;n -> 尝试n次后休眠
;.....

;-1 -> 一直尝试，直到达到期望值（慎用）

MaxContinueNum = 2




;刷到300首后停止
;会多一份请求，默认开启
Enable300 = True

;没有部分多线程的日志(还是有日志) 可以认真查看已经刷了多少听歌量了
;平常没必要开，DEBUG的时候需要开启
NoThreadLogs = True

;期望值，若达不到期望值则会推倒重来
ExpectationNum = 250


;给网易云喘息的机会，不然容易风控，如果你觉得影响效率可适当降低此数值
;(主要原因是多线程吃带宽太快了，会影响听歌量的获取，若你没有开启Enable300则可以忽视)
SleepTime = 1.3

;忽略UID解析错误提示，将在提示过后自动变为True
IgnoreUidError = True

;浏览器(Chrome/Firefox/Edge/Safari)
browser = Chrome

------------

### 注意事项
> 请勿泄露你的cookie，免费软件禁止商用
