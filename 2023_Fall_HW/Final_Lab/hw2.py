import numpy as np
import matplotlib.pyplot as plt

def calculate_collision_probability(num_devices, num_channels, num_iterations):
    collision_probabilities = np.zeros(num_channels)

    for i in range(num_iterations):
        # Generate random channel selections for each device
        channel_selections = np.random.choice(num_channels, num_devices, replace=True)

        # Count the number of devices on each channel
        channel_counts = np.bincount(channel_selections, minlength=num_channels)

        # Calculate collision probability for each channel
        collision_probabilities += (channel_counts > 1).astype(int)


    # Average collision probability over all iterations
    average_collision_probabilities = collision_probabilities / num_iterations

    return average_collision_probabilities

def plot_probability_distribution(probabilities):
    channels = np.arange(1, len(probabilities) + 1)
    plt.bar(channels, probabilities)
    plt.xlabel('Channel')
    plt.ylabel('Collision Probability')
    plt.title('Collision Probability Distribution')
    plt.show()

# Parameters
num_devices = 20
num_channels = 79
# The hopping rate is 1600 hops/sec or 0.625ms per slot
hopping_rate = 1600

# stable for 30 seconds
time = 30

num_iterations = time * hopping_rate

# Calculate collision probabilities
collision_probabilities = calculate_collision_probability(num_devices, num_channels, num_iterations)

# Calculate and print the average collision probability across all channels
average_collision_probability = np.mean(collision_probabilities)
print(f'Average Collision Probability: {average_collision_probability:.4f}')

# Plot the probability distribution
plot_probability_distribution(collision_probabilities)