# -*- coding: UTF-8 -*-
from math import floor
import time
import threading
#
#     设定
#     单用户每次拉到10人助力，其中5人为新消用户，3人转化
#     客单价为10元，
# ###



class Customer(threading.Thread):

    def __init__(self,queue,father=None):     #拉新的初始用户
        threading.Thread.__init__(self)
        self.isNew = True
        self.bonus = 0
        self.father = father
        self.queue = queue
        self.order_sum = 0


    def setOld(self):    #转化
        self.isNew = False

    def getNewBonus(self,nbonus): #拉新奖励
        self.bonus += nbonus

    def consume(self,orde_price,old_user,old_bonus,new_scan,new_bonus,new_t_bonus):
        self.order_sum += orde_price - min(orde_price/2.0,self.bonus/2.0)   #单次消费的可用奖励金最高不超过订单价格一半及或提现的奖励金全额的一半

        if self.isNew == True:                                               #新用户转化，拉新奖励给回到发展人
            if self.father is not None:
                self.father.bonus += new_t_bonus
            self.setOld()

        #分享浏览奖励金
        self.bonus = old_user * old_bonus + new_bonus * new_scan

        self.bringNewCustomer(0.6,5)


    def bringNewCustomer(self,transfer_rate,new_scan,squeu):             #拉新转化

        for i in range(floor(new_scan*transfer_rate)):
            self.queue.put(Customer(self))


    def run(self):
        while(True):
            self.consume()
            time.sleep(1)



if __name__ == "__main__":
    old_set= []
    for i in range(0, 10):
        old_set.append(Customer().start())


