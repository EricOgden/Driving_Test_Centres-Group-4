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
data = data.dropna(subset=['Covid Traffic', 'Covid Pass Rates', 'Covid Test Centres'])

data['Covid Traffic'] = pd.to_numeric(data['Covid Traffic'], errors='coerce')
data['Covid Pass Rates'] = pd.to_numeric(data['Covid Pass Rates'], errors='coerce')
data = data.dropna(subset=['Covid Traffic', 'Covid Pass Rates'])
data = data[np.isfinite(data['Covid Traffic']) & np.isfinite(data['Covid Pass Rates'])]

#Seperation for high and low pass rates
x = 50  
high_pass = data[data['Covid Pass Rates'] >= x]
low_pass = data[data['Covid Pass Rates'] < x]

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(data['Covid Traffic'], data['Covid Pass Rates'], color='blue', marker='x', s=500, alpha=0.7)

# Function to create an ellipse around a cluster
def plot_ellipse(ax, x, y, color, alpha=0.3, scale_factor=6):
    if len(x) > 2:  # Ensure there are enough points to form a cluster
        cov = np.cov(x, y)  # Get covariance matrix
        if np.any(np.isnan(cov)) or np.any(np.isinf(cov)):  # Check for numerical issues
            return
        lambda_, v = np.linalg.eig(cov)
        lambda_ = np.sqrt(lambda_)  # Standard deviation scaling
        ellipse = Ellipse(
            xy=(np.mean(x), np.mean(y)),
            width=lambda_[0] * scale_factor,  # Scale factor for visualization
            height=lambda_[1] * scale_factor,
            angle=np.rad2deg(np.arccos(v[0, 0])),
            edgecolor='none',
            facecolor=color,
            alpha=alpha
        )
        ax.add_patch(ellipse)

plot_ellipse(ax, high_pass['Covid Traffic'], high_pass['Covid Pass Rates'], color='green', scale_factor=8)
plot_ellipse(ax, low_pass['Covid Traffic'], low_pass['Covid Pass Rates'], color='red', scale_factor=6)
"""
For some reason python would automatically scale the axis. So this had to be
done to ensure the x-axis stayed >0
"""
ax.set_xlim(left=0)

# Add title, labels and save
ax.set_title('Pass Rates vs Annual Traffic During Covid', fontsize=22)
ax.set_xlabel('All Motorvehicles During Covid', fontsize=15)
ax.set_ylabel('Pass Rate (%)', fontsize=15)
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("covid_scatter_plot_final_perfect.png", dpi=300)
plt.show()
