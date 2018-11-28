# -*- coding: UTF-8 -*-
from math import floor
import time
import threading
import queue
import uuid
#
#     设定
#     单用户每次拉到10人助力，其中5人为新消用户，3人转化
#     客单价为10元，
# ###



class Customer(threading.Thread):

    def __init__(self,queue,father=None):     #拉新的初始用户
        threading.Thread.__init__(self)
        self.id = uuid.uuid4() 
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



    def bringNewCustomer(self,transfer_rate,new_scan):             #拉新转化

        for i in range(floor(new_scan*transfer_rate)):
            self.queue.put(Customer(self.queue,self))


    def run(self):
        while(True):
            self.consume(10,5,0.5,5,3,5)
            self.bringNewCustomer(0.6,5)
            print("id:%s  order:%d bonus:%d"%(self.id,self.order_sum,self.bonus))
            time.sleep(10)



if __name__ == "__main__":
    L = []
    q = queue.Queue()
    for i in range(10):
        item=(Customer(q))
        q.put(item)
        print("new Customer")
    try:   
        while not q.empty():
            item = q.get()
            L.append(item)
            item.start()
            # time.sleep(1)
    except KeyboardInterrupt:
        print("customer num:%d" % len(L))
        print("customer order_sum:%d" % sum(i.order_sum for i in L))
        print("customer bonus_sum:%d" % sum(i.bonus for i in L))
