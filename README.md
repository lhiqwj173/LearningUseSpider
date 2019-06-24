# asyncio库的使用

自python3.6后，异步框架以得官方扶正，我也很少再用requests模块了

协程无线程切换开销，理论上比多进程+多线程快，即使是单线程，协程的速度也不容小觑

而python有所谓的线程锁，所以不知是否能达到真正的多线程速度，而协程则无限制条件

aiohttp是requests的异步架构

aiofiles虽然说是异步读写，但听说底层的写入还是同步的，但一但代码确定使用异步，所有的都得异步

异步框架爬虫基本采取生产者消费者模型，入与取

依赖
```
- aiofiles
- aiohttp
- multiprocessing //多进程加速
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
