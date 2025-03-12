import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the path to the JSON file
json_file_path = 'results_sorted.json'

# For the second json file
# json_file_path = 'results_sorted_random.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    data = json.load(file)

locations = list(data.keys())
roundabout_counts = [data[loc]["roundabout_count"] for loc in locations]
mini_roundabout_counts = [data[loc]["mini_roundabout_count"] for loc in locations]
dual_carriageway_counts = [data[loc]["dual_carriageway_count"] for loc in locations]
all_junction_counts = [data[loc]["all_junction_count"] for loc in locations]


# Find the index of 'Belvedere'
belvedere_index = locations.index('Luton')

# Plotting
fig, axs = plt.subplots(3, 2, figsize=(14, 15))

# Function to add vertical line and background color
def add_split(ax, index):
    ax.axvline(x=index - 0.5, color='grey', linestyle='--')
    ax.axvspan(-0.5, index - 0.5, color='lightgreen', alpha=0.4)
    ax.axvspan(index - 0.5, len(locations) - 0.5, color='lightcoral', alpha=0.4)

# Create custom legend entries
green_patch = mpatches.Patch(color='lightgreen', alpha=0.4, label='Top 10 pass rates')
red_patch = mpatches.Patch(color='lightcoral', alpha=0.4, label='Bottom 10 pass rates')


# Plotting the first figure
fig1, axs1 = plt.subplots(2, 1, figsize=(14, 10))

# Roundabout Count
axs1[0].bar(locations, roundabout_counts, color='darkblue')
axs1[0].set_title('Major Roundabouts')
axs1[0].set_xlabel('Test Centre')
axs1[0].set_ylabel('Count')
axs1[0].set_xticklabels(locations, rotation=90)
axs1[0].yaxis.tick_right()
axs1[0].yaxis.set_label_position("right")
axs1[0].set_xlim(-0.5, len(locations) - 0.5)  # Adjust xlim to remove whitespace
add_split(axs1[0], belvedere_index)

# Mini Roundabout Count
axs1[1].bar(locations, mini_roundabout_counts, color='darkblue')
axs1[1].set_title('Mini Roundabouts')
axs1[1].set_xlabel('Test Centre')
axs1[1].set_ylabel('Count')
axs1[1].set_xticklabels(locations, rotation=90)
axs1[1].yaxis.tick_right()
axs1[1].yaxis.set_label_position("right")
axs1[1].set_xlim(-0.5, len(locations) - 0.5)
add_split(axs1[1], belvedere_index)

# Adding custom legend
fig1.legend(handles=[green_patch, red_patch], loc='upper right')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('road_features_roundabouts.png')


# Plotting the second figure
fig2, axs2 = plt.subplots(2, 1, figsize=(14, 10))

# Dual Carriageway Count
axs2[0].bar(locations, dual_carriageway_counts, color='darkblue')
axs2[0].set_title('Dual Carriageways')
axs2[0].set_xlabel('Test Centre')
axs2[0].set_ylabel('Count')
axs2[0].set_xticklabels(locations, rotation=90)
axs2[0].yaxis.tick_right()
axs2[0].yaxis.set_label_position("right")
axs2[0].set_xlim(-0.5, len(locations) - 0.5)
add_split(axs2[0], belvedere_index)

# All Junction Count
axs2[1].bar(locations, all_junction_counts, color='darkblue')
axs2[1].set_title('All Junctions')
axs2[1].set_xlabel('Test Centre')
axs2[1].set_ylabel('Count')
axs2[1].set_xticklabels(locations, rotation=90)
axs2[1].yaxis.tick_right()
axs2[1].yaxis.set_label_position("right")
axs2[1].set_xlim(-0.5, len(locations) - 0.5)
add_split(axs2[1], belvedere_index)

# Adding custom legend
fig2.legend(handles=[green_patch, red_patch], loc='upper right')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('road_features_roadtype.png')


# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.savefig('road_features.png')
# plt.show()