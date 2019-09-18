# asyncio库的使用

自python3.6后，异步框架以得官方扶正，我也很少再用requests模块了

协程无线程切换开销，理论上比多进程+多线程快，即使是单线程，协程的速度也不容小觑

而python有所谓的线程锁，所以不知是否能达到真正的多线程速度，而协程....（有没有我也不知道（笑））

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
- 自行修改消费者（协程）数，建议 协程x进程 不超过16为宜，8核CPU即开2个消费者线程，单核即可开16个
- 若消费者数量大于队列上限，请自行修改

运行:
```
python3 *.py

python3 xvideos.py <tag>
python3 fc2ppv.py <num>   <num>为从第几页开始爬取
```

```
C:\Users\Jackyao\Desktop\test\dist>fc2ppv.exe -h
usage: fc2ppv.py [-h] [-p n] [-b n n] [-a]

downloader for fc2ppvfanclub picture

optional arguments:
  -h, --help            show this help message and exit
  -p n, --page n        which page to crawl(clash with -b -a), example: -p 12
  -b n n, --between n n
                        page between a and b(include, clash with -p -a),
                        example: -b 2 3
  -a, --all             this flag would download all the page(clash with -p
                        -b)

```
