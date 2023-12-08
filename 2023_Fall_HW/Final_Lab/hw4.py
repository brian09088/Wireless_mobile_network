import random
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

NUM_CHANNELS = 79

threshold_num = [0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9]

def wmn_hw_3():
    channel = [0]*79  #先全部設為bad channel
    good_channel_count = 0
    temp = 0.1
    while(good_channel_count<39):
        set_good = random.randint(0,78)  #從陣列0-78中
        if(channel[set_good] == 1):
            continue
        else:
            channel[set_good] == 1   #設為good channel
            good_channel_count += 1
            
    for i in range(79):
        if(channel[i] == 0):
            set_good = poisson.rvs(mu=0.4 , size=1)
            #print(set_good)
            if(set_good[0] == 0):
                channel[i] = 1
    channel_2 = []

    channel_occupy = [0]*79      #記每個channel連續被占領的hop次數    
    device_in_channel = [0]*79   #記每個channel有幾個device

    for device in range(25,90,25):    #25、50、75

        device_collision = [0]*9
        device_collision_probability = []
        print("-----------------------------")
        print("裝置數:",device)
        for threshold in range(9):    #0.1、0.2、0.3、0.4...0.9

            # 此channel有device超過此hop數即為bad channel
            threshold_hop = (threshold+1) * 4 * 160

            device_collision = [0]*9
            for i in range(79):
                channel_2.append(channel[i])
            for i in range(8000):    #前5秒，1600*5=8000

                for k in range(79):       #確認每個channel是否超過門檻
                    if(channel_occupy[k] == threshold_hop and channel_2[k] == 1):   #達到門檻值且原本為good channel
                        channel_2[k] = 0   #設為bad channel

                device_in_channel = [0]*79     #新hop中，每個channel都沒有device

                for j in range(device):       #第j+1個device                  
                    jump_to = random.randint(0,78)  #跳到某隨機channel
                    if(device_in_channel[jump_to] !=0 ):  #選到的channel已有device
                        device_in_channel[jump_to] += 1    #選到的channel上的device+1   
                    elif(device_in_channel[jump_to] == 0):   #選到的channel沒有device
                        device_in_channel[jump_to] = 1       #設此channel為有device
                        channel_occupy[jump_to] += 1          #此channel佔據次數+1

            print("bad channel門檻值:" , threshold_hop ," bad channel 數量:" , channel_2.count(0) ,"\n")        
            
            device_in_channel = [0]*79   #記每個channel有沒有device
            for i in range(40000):     #後25秒
                
                for j in range(device):       #第j+1個device      
                    offset_right = 0
                    offset_left = 0
                    jump_to = random.randint(0,78)  #跳到某隨機channel
                    temp = 78-jump_to

                    if(device_in_channel[jump_to] == 1):     #選到的channel已有device
                        device_collision[threshold] += 1

                        if(channel_2[jump_to] == 0):   #跳到bad
                            for r in range(0,temp):    #r=1~temp-1
                                if(temp == 0):
                                    offset_right = 0
                                elif(channel_2[jump_to + r] == 1):   #往右邊最近的good channel
                                    offset_right = r

                            for l in range(0,jump_to):  #l=1~jump_to-1
                                if(jump_to == 0):
                                    offset_left = 0
                                elif(channel_2[jump_to - l] == 1):   #往左邊最近的good channel
                                    offset_left = l
                                    
                            if(offset_right < offset_left):   #往右跳

                                device_in_channel[jump_to + offset_right] += 1
                            elif(offset_right > offset_left):
                                device_in_channel[jump_to - offset_left] += 1
                            else:
                                device_in_channel[jump_to] = 1
                        else:     #跳到good
                            device_in_channel[jump_to] += 1
                    elif(device_in_channel[jump_to] > 1):
                        continue
                    else:       #選到的channel無device
                        device_in_channel[jump_to] = 1 
                device_in_channel = [0]*79   #新hop前，每個channel沒有device

            channel_2 = []
            channel_occupy = [0]*79      #記每個channel連續被占領的hop次數    
            device_in_channel = [0]*79   #記每個channel有沒有device
            print("碰撞次數:", device_collision[threshold] , "機率:" , device_collision[threshold]/(40000*79))
            device_collision_probability.append(device_collision[threshold]/(40000*79))

        plt.plot(threshold_num, device_collision_probability)
        plt.xlabel("Threshold")
        plt.ylabel("Device collision propobility")
        plt.savefig(str(device) + ' devices Threshhold & collision_rate.png', dpi=300, bbox_inches='tight')
        plt.clf()
        plt.close()

# 執行hw3程式碼
wmn_hw_3()