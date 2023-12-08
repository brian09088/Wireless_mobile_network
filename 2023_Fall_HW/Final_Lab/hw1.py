import random
import matplotlib.pyplot as plt

# hopping rate is 1600 hops/sec or 0.625ms per slot
backoff = 625
hopping_rate = 1600
NUM_CHANNELS = 79
hopping_rate = 1600
# 1600*30=48000
NUM_SIMULATIONS = 48000


# Q1: 2 devices
def simulate_two_devices():
    collisions = 0
    for i in range(NUM_SIMULATIONS):
        channel1 = random.randint(0, NUM_CHANNELS-1) 
        channel2 = random.randint(0, NUM_CHANNELS-1)
        if channel1 == channel2:
            collisions += 1
    return collisions / NUM_SIMULATIONS

# Q1 : 2 devices (simulation of 100萬次 iteration)
# average collision probability ~= 1.3% (p = 0.013) 
prob_two_devices = simulate_two_devices()
print(f"Average collision probability for two devices: {prob_two_devices:.3f}")

# Q2 : 20 devices (simulation of 100萬次 iteration)
# average collision probability ~= 26.2% (p = 0.262) 
# prob_twenty_devices = simulate_multiple_devices(20) 
# print(f"Average collision probability for twenty devices: {prob_twenty_devices:.3f}")