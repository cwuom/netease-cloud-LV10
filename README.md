<div align="center">
   <img width="500" src="LOGO.png" alt="logo"></br>


# **NeteaseCloudMusicTools**   - 网易云升级助手

**NeteaseCloudMusicTools是一个可以在Windows平台上运行的全自动网易云刷等级脚本兼工具箱!**

**基于[Python3.7](https://www.python.org/downloads/release/python-370/ "Python3.7")编写**

</div>

----

#### bilibili -[ im-cwuom](https://space.bilibili.com/473400804?spm_id_from=333.1007.0.0 " im-cwuom") 关注我获取更多!

------------



### 关于NeteaseCloudMusicTools
#### 功能方面
- 每天(9点)稳定300首 + 自动签到
- 支持三种刷单曲听歌量需求
- 可根据自己的升级需求来更改单独配置
- 刷到300首自动终止
- 当听歌量无法满足时自动重试
- 自动启用api服务
- 下载歌曲 / 歌单 无损解析(VIP)
- 听歌量进度缓存，防止意外终止
- 直接使用现有 cookie 登录指定浏览器
- 配置文件损坏自动修复
- ...
------------
#### 登录方面
- 支持qrlogin(扫码登录)自动获取cookie
- 支持调起多种主流浏览器(Chrome/Firefox/Edge/Safari)
- 当cookie失效时自动重新要求登录
------------
### 效率方面
#### 运行
- 所有方案基本采用多线程

#### 升级
- LV9的账户 300 首刷满大约 3min 较低等级 1-2min 左右 

#### 单曲听歌量
-  模式二可在60s左右可达到100 ~ 1000+单曲听歌量增长

------------

#### 支持的平台
- 打包版本目前只支持windows，但源码可以复制到linux主机上(前提: 有py环境, 模块正常)

------------

### 便携性/兼容性
- 操作简单，哪怕没有基础也可以快速部署，因为看见有人收费所以想着自己做了一个，但网上大多数升级工具(除收费，网站版)部署困难，但此程序已经整合了所需环境，双击打开就可运行
- 不兼容Windows 7或老架构的机器，测试环境Windows 11 专业版 22H2


------------

### 有演示吗?
*[一个无脑到不行的网易云辅助项目，能让你的年度听歌惊呆众人](https://www.bilibili.com/video/BV1224y1t7hf/?spm_id_from=333.999.0.0 "一个无脑到不行的网易云辅助项目，能让你的年度听歌惊呆众人")*


------------

### 我该如何在Linux/服务器上使用它？
#### 注意
- 软件在非必要时不会提供Linux版本，但并不代表无法使用，下列会给出在Linux/服务器上部署此项目的方法
- NeteaseCloudMusicTools1.5b已在Debian上测试通过，但最新版本往往不会第一时间放在上述环境中测试，若要使用还需自行折腾
- 在此环境中不能保证所有功能能够正常使用

#### 使用
1. 在[Releases](https://github.com/cwuom/netease-cloud-LV10/releases "Releases")中下载main_exe.py(下述简称文件)
2. 将文件转移到你的Linux主机
3. 将cookie.txt转移到文件所在目录
4. 下载文件所需模块
5. 手动启动node服务，在[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi "NeteaseCloudMusicApi")中查看详细教程
6. 准备完毕，在终端启动文件
7. 正常使用

------------


### 脚本截图
[![s1](https://raw.githubusercontent.com/cwuom/netease-cloud-LV10/main/s1.png "s1")](https://raw.githubusercontent.com/cwuom/netease-cloud-LV10/main/s1.png "s1")


------------

## 声明
### 一切开发旨在学习，请勿用于非法用途
- NeteaseCloudMusicTools是一个完全免费的软件，仅供娱乐使用
- NeteaseCloudMusicTools不会对任何人采取收费行为，如果你希望它更好，可以赞助此项目
- 介于项目的特殊性，开发者可能在未来会随时停更或删除此项目
- 软件运行不会窃取你的cookie，如果账户被盗请不要找我，首先检查分享时cookie是否清空
