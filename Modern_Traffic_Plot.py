import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

file_path = "data.xlsx"  
data = pd.read_excel(file_path)
"""
The website we used to collect the traffic data didnt have much info for the 
more rural test centres so we had to ignore a few.
"""
data = data.dropna(subset=['all_mv', 'Pass Rate', 'Test Centre'])

data['all_mv'] = pd.to_numeric(data['all_mv'], errors='coerce')
data['Pass Rate'] = pd.to_numeric(data['Pass Rate'], errors='coerce')

#Seperation for high and low pass rates
x = 50  
high_pass = data[data['Pass Rate'] >= x]
low_pass = data[data['Pass Rate'] < x]

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(data['all_mv'], data['Pass Rate'], color='blue', marker='x', s=350, alpha=0.7)

# Function to create a shaded reigon around a cluster
def plot_ellipse(ax, x, y, color, alpha=0.3):
    if len(x) > 2:  # Ensure there are enough points to form a cluster
        cov = np.cov(x, y)  # Get covariance matrix
        if np.any(np.isnan(cov)) or np.any(np.isinf(cov)):  # Check for numerical issues
            return
        lambda_, v = np.linalg.eig(cov)
        lambda_ = np.sqrt(lambda_)  # Standard deviation scaling
        ellipse = Ellipse(
            xy=(np.mean(x), np.mean(y)),
            width=lambda_[0] * 6,  # Scale factor for visualization
            height=lambda_[1] * 6,
            angle=np.rad2deg(np.arccos(v[0, 0])),
            edgecolor='none',
            facecolor=color,
            alpha=alpha
        )
        ax.add_patch(ellipse)

plot_ellipse(ax, high_pass['all_mv'], high_pass['Pass Rate'], color='green')
plot_ellipse(ax, low_pass['all_mv'], low_pass['Pass Rate'], color='red')
"""
For some reason python would automatically scale the axis. So this had to be
done to ensure the x-axis stayed >0
"""
ax.set_xlim(left=0)

# Add title, labels and save 
ax.set_title('Pass Rates vs Annual Traffic (2023-2024)', fontsize=22)
ax.set_xlabel('All Motorvehicles', fontsize=15)
ax.set_ylabel('Pass Rate (%)', fontsize=15)
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("scatter_plot.png", dpi=300)
plt.show()


