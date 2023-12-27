import random
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

def wmn_hw3():
    channel = [0]*79  #先全部設為bad channel
    good_channel_count = 0
    channel_ID = []
    channel_collision_probability = []
    threshold_num = []
    bad_channel = []
    temp = 0.0
    while(good_channel_count<39):
        set_good = random.randint(0,78)  #從陣列0-78中隨機
        if(channel[set_good] == 1):
            continue
        else:
            channel[set_good] == 1   #設為good channel
            good_channel_count += 1  #good channel count 總共39個
    for i in range(79):
        if(channel[i] == 0):
            set_good = poisson.rvs(mu=16 , size=1) # poisson分布 p=0.4, mu=40*0.4=16
            if(set_good[0] == 0):
                channel[i] = 1
    channel_collision = [0]*79   #記每個channel發生幾次碰撞
    channel_occupy = [0]*79      #記每個channel連續被占領的hop次數    
    device_in_channel = [0]*79   #記每個channel有幾個device
    channel_2 = []
    
    for device in range(25,90,25):    #25、50、75
        threshold = 1
        temp=0.0
        channel_ID = []
        channel_collision_probability = []
        threshold_num = []
        bad_channel = []

        while(threshold < 10):    #0.1、0.2、0.3、0.4...0.9
            threshold_hop = threshold*3*1600   #此channel有device超過此hop數即為bad channel
            channel_collision = [0]*79
            for i in range(79):
                channel_2.append(channel[i])
            for i in range(48000):        #在0~47999 hop時
                for k in range(79):       #確認每個channel是否現在有device
                    if(device_in_channel[k] != 0 ):   #此channel有device
                        if(channel_occupy[k] == threshold_hop and channel_2[k] == 1):   #達到門檻值且原本為good channel
                            channel_2[k] = 0   #設為bad channel
                device_in_channel = [0]*79     #新hop中，每個channel都沒有device
                        
                for j in range(device):       #第j+1個device                  
                    jump_to = random.randint(0, 78)  #跳到某隨機channel
                    if(device_in_channel[jump_to] == 1 ):  #選到的channel已有一部device
                        channel_collision[jump_to] += 1    #發生碰撞
                        device_in_channel[jump_to] += 1    #選到的channel上的device+1
                    elif(device_in_channel[jump_to] > 1 ):    #選到的channel已有超過一部device
                        continue     
                    elif(device_in_channel[jump_to] == 0):   #選到的channel沒有device
                        device_in_channel[jump_to] = 1       #設此channel為有device
                        channel_occupy[jump_to] += 1          #此channel佔據次數+1

            temp += 0.1
            threshold_num.append(temp)
            bad_channel.append(channel_2.count(0))

            threshold += 1
            channel_2 = []
            channel_occupy = [0]*79      #記每個channel連續被占領的hop次數    
            device_in_channel = [0]*79   #記每個channel有沒有device
        
        for i in range(79):   #輸出每個channel的總碰撞次數
            channel_ID.append(i+1)
            channel_collision_probability.append(channel_collision[i]/48000)

        plt.plot(channel_ID , channel_collision_probability)
        plt.xlabel("Channel ID")
        plt.ylabel("Channel collision propobility")
        plt.savefig(str(device)+' device.png', dpi=300, bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.plot(threshold_num , bad_channel)
        plt.xlabel("Threshold")
        plt.ylabel("Bad channels")
        plt.savefig(str(device) +' device threshold & bad_channels.png', dpi=300, bbox_inches='tight')
        plt.clf()
        plt.close()
        
wmn_hw3()