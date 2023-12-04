import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Step 1: Specify the path to your CSV file
csv_file_path = "BTC-USD.csv"

# Step 2: Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Step 3: Create a figure and axes for the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Initial number of displayed x-axis values
initial_display = len(df['Date']) // 10

# Plot the closing values
line, = ax.plot(df['Date'][:initial_display], df['Close'][:initial_display], label='Closing Value', marker='o', linestyle='-')

# Customize the plot
ax.set_title('Closing Values Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Value')
ax.legend()
ax.grid(True)
fig.tight_layout()

# Add a slider
ax_slider = plt.axes([0.1, 0.02, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Show N Dates', valmin=1, valmax=len(df['Date']), valinit=initial_display, valstep=1)

# Slider update function
def update(val):
    n_dates = int(slider.val)
    line.set_xdata(df['Date'][:n_dates])
    line.set_ydata(df['Close'][:n_dates])
    fig.canvas.draw_idle()

# Connect the slider to the update function
slider.on_changed(update)

# Show the plot
plt.show()
