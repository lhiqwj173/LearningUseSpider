#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: notepad++
# @Date: 2019-07-02 星期二 11:40
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期二 16:15

import random
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
import numpy as np
from dataclasses import dataclass

@dataclass()
class morraGame(object):
    name: str = 'Nobody'
    times: int = 100
    loseCount = 0
    winCount = 0
    middleCount = 0
    guessCount = 0
    x = []
    y1 = []
    p2 = []
    s3 = []
    morraList = (['0', '1', '2'])
    winList = (['0','1'],['1','2'],['2','0'])

    def bothGuess(self):
        """双方猜拳"""
        pcChoiceSelf = random.choice(self.morraList) #玩家，考虑手动输入次数太多，也让电脑选
        pcChoice = random.choice(self.morraList)
        
        #增加猜拳次数
        self.guessCount += 1
        # 返回结果
        return [pcChoiceSelf,pcChoice]
    
    def winOrlost(self):
        """判断输平赢"""
        answer = self.bothGuess()
        if answer in self.winList:
            self.winCount += 1
        elif answer[0] == answer [1]:
            self.middleCount += 1
        else:
            self.loseCount += 1
    
    def getNowResult(self):
        """取得图表数据"""
        return [self.winCount,self.middleCount,self.loseCount, self.guessCount]
    
    def writeResult(self):
        """写入文件结果"""
        with open("result.txt", 'a+') as file:
            file.write(f"共进行{self.guessCount}次游戏, {self.name}共计赢{self.winCount}，输{self.loseCount}，平{self.middleCount}\n")
    
    def start(self):
        """开始游戏"""
        for _ in range(self.times):
            self.winOrlost()
            
            #每20次统计结果
            if self.guessCount%(self.times*0.1) == 0:
                self.writeResult()
                tmp = self.getNowResult()
                self.y1.append(tmp[0])
                self.p2.append(tmp[1])
                self.s3.append(tmp[2])
                self.x.append(tmp[3])
        #print(self.x)
        
    def matplotlibShow(self):
        """图表显示保存"""
        x = np.array(self.x) #将数组转换成array，方便加减
        bar_width=self.times*0.01 #设置柱状图的宽度
        tick_label=[str(_)+'次' for _ in self.x] #x轴标签

        #绘制并列柱状图
        plt.bar(x,self.y1,bar_width,color='salmon',label='赢')
        plt.bar(x+bar_width,self.p2,bar_width,color='orchid',label='平')
        plt.bar(x+bar_width+bar_width,self.s3,bar_width,color='blue',label='输')

        plt.legend()#显示图例，即label赢平输
        plt.xticks(x+bar_width, tick_label)#显示x坐标轴的标签,调整位置
        #plt.show()
        plt.savefig("result.png")
    
if __name__ == "__main__":
    a = morraGame('John', 10000)
    a.start()
    a.matplotlibShow()
    #b = morraGame('two', 1000)
    #b.start()
    
