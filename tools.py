from dataclasses import dataclass
import aiohttp
import os
import aiofiles
import asyncio

@dataclass()
class Web(object):
    url: str
    proxy: str = 'http://127.0.0.1:1080'

    @classmethod
    def mkDir(self):
        if not os.path.exists('./download'):
            os.mkdir("./download")

    async def fetch(self, data=False):
        """解析函数"""
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(self.url, proxy=self.proxy, verify_ssl=False) as r:
                    if data:
                        return await r.read()
                    else:
                        return await r.text()
        except asyncio.TimeoutError:
            print("Time out")

    async def getHtmlCode(self):
        return await self.fetch()

    async def getByte(self):
        return await self.fetch(data=True)

    async def saveFile(self):
        """文件下载函数"""
        Web.mkDir()
        async with aiofiles.open(f'./download/{self.url.split("/")[-1]}', 'wb') as f:
            await f.write(await self.getByte())



