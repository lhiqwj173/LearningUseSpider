# 练习PyQuery的使用

代码来自两个爬虫，都是用来下载图片与漫画的（现以无法确定是否能使用）

框架基本一样，采用多进程加速下载，但没有异常处理。

之前一直在使用`BeautifulSoup`，但听说解析速度相对还是`PyQuery`更快一点就换掉了，

然而我并不能明显的感觉出来快多少。

程序依赖模块:
- requests
- pyquery
- multiprocess

安装:
```
pip3 install requests
pip3 install pyquery
pip3 install multiprocess
```

使用:
- 需要修改下载路径
- 解析代码换一换就可以直接套在别的站点了

运行:
```
python3 hswyc.py
/
python3 yxanimetion.py
```

# asyncio库的使用

自python3.6后，异步框架以得官方扶正，我也很少再用request同步模块了
aiohttp是request的异步架构
aiofiles虽然说是异步读写，但听说速度不比同步快多少
异步框架基本采取生产者消费者模式，创建队列，入与取。

依赖
```
- aiofiles
- aiohttp
- uvloop //windows不可用
```
使用:
- 网址
- 路径

运行:
```
python3 .py url path
```
各个目录路径需自行创建
