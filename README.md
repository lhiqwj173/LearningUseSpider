# 练习PyQuery的使用

代码来自两个爬虫，都是用来下载图片与漫画的。

框架基本一样，采用多进程加速下载，但没有异常处理。

之前一直在使用`BeautifulSoup`，但听说解析速度相对还是`PyQuery`更快一点就换掉了，

然而我并不能明显的感觉出来快多少。

程序依赖模块:
- requests
- pyquery
- multiprocess

安装:
```Python
pip3 install requests
pip3 install pyquery
pip3 install multiprocess
```