import random
import matplotlib.pyplot as plt
from scipy.stats import poisson
import numpy as np

NUM_CHANNELS = 79
threshold_num = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def initialize_channels():
    # Initialize channels
    channels = [1] * 39 + [0] * 40

    # Set bad channels using Poisson
    for i in range(39, 79):
        rnd = poisson.rvs(0.4)
        if rnd == 0:
            channels[i] = 1

    return channels


def simulate_timestep(channels, device_count):
    # Simulate device_count devices
    collisions = [0] * 79
    for i in range(device_count):
        ch = random.randint(0, 78)
        collisions[ch] += 1

    return collisions

def wmn_hw3():
    for device_count in [25, 50, 75]:

        channels = initialize_channels()
        bad_channels = []

        print(f"{device_count} devices:")

        for threshold in threshold_num:

            # Reset collisions for each threshold
            collision_prob = [0] * NUM_CHANNELS

            # Run simulation
            for t in range(48000):
                current_collisions = simulate_timestep(channels, device_count)
                collision_prob = [x + y for x, y in zip(collision_prob, current_collisions)]

            # Calculate collision probability per channel
            prob_per_channel = [c / 48000 for c in collision_prob]

            # Identify bad channels
            bad_channels_count = sum(1 for prob, corruption in zip(prob_per_channel, channels[39:]) if prob > threshold and corruption == 1)
            bad_channels.append(bad_channels_count)

            print(f"Threshold {threshold}: {bad_channels_count} bad channels")

        # Plot 1 - Collision probability per channel
        plt.plot(range(1, NUM_CHANNELS + 1), prob_per_channel)  # Adjusted x-axis range
        plt.title(f"{device_count} devices")
        plt.xlabel("Channels")
        plt.ylabel("Collision Probability")
        plt.savefig(f"{device_count} collision_probability")
        plt.clf()  # Clear the plot for the next iteration

        # Plot 2 - Bad channels vs threshold
        plt.plot(threshold_num, bad_channels)
        plt.title(f"{device_count} devices")
        plt.xlabel("Threshold")
        plt.ylabel("Bad Channels")
        plt.savefig(f"{device_count} threshold_bad_channels")
        plt.clf()  # Clear the plot for the next iteration

    print("Simulation complete!")

# Run the simulation
wmn_hw3()
