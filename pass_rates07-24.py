import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Read the file containing years, the number of driving tests conducted each year, and the pass rates for each year
df = pd.read_csv("passrates07-24.csv")

x = df.iloc[:, 1] # years
hist = df.iloc[:, 2] # driving tests conducted
y = df.iloc[:, 3] # pass rates

print(df.head)

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.bar(x, hist, width=0.8, alpha=1, color='steelblue', label="Driving Tests Conducted")
ax1.set_xlabel("Time (years)")
ax1.set_ylabel("Driving Tests Conducted", color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax1.set_yticks(range(0, 2000001, 250000))

ax2 = ax1.twinx()
ax2.plot(x, y, marker='o', linestyle='-', color='r', label="Pass Rate (%)")
ax2.set_ylabel("Pass Rate (%)", color='r')
ax2.tick_params(axis='y', labelcolor='r')

ax2.set_ylim(0, 60)

plt.title("Driving Tests Conducted and Pass Rates")
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.show()
