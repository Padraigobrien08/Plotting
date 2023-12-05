import pandas as pd
from matplotlib.widgets import RangeSlider
import matplotlib.pyplot as plt

# Read the CSV data
df = pd.read_csv("BTC-USD.csv")
# Create a new figure for the dynamic plot
fig, ax = plt.subplots(figsize=(15, 6))

# Initial window size and position
initial_window_size = 100
initial_window_pos = 0

# Plot the closing values for the initial window
line, = ax.plot(df['Date'][initial_window_pos:initial_window_pos + initial_window_size],
                df['Close'][initial_window_pos:initial_window_pos + initial_window_size],
                label='Closing Value',
                linestyle='-')

# Customize the plot
ax.set_title('Closing Values Over Time')
x_ticks_interval = max(1, initial_window_size // 20)
ax.set_xticks(df.index[initial_window_pos:initial_window_pos + initial_window_size:x_ticks_interval])
ax.set_xticklabels(df['Date'].iloc[df.index[initial_window_pos:initial_window_pos + initial_window_size:x_ticks_interval]], rotation=45, ha='right')

ax.set_ylabel('Closing Value')
plt.grid(True)
ax.legend()
fig.tight_layout()

# Add a RangeSlider with two thumbs for selecting the window
ax_slider_range = plt.axes([0.1, 0.02, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider_range = RangeSlider(ax_slider_range, 'Show N Dates', valmin=1, valmax=len(df['Date']),
                           valinit=[initial_window_pos, initial_window_pos + initial_window_size], valstep=1)
# Slider update function
def update(val):
    window_pos = [int(i) for i in slider_range.val]
    window_size = window_pos[1] - window_pos[0]

    # Calculate proper window position and size
    if window_size >= len(df):
        window_pos = [0, len(df) - 1]
        window_size = len(df)

    # Sort the data based on the index
    sorted_indices = df.index.argsort()
    sorted_close = df['Close'].iloc[sorted_indices]
    sorted_high = df['High'].iloc[sorted_indices]

    # Update x-axis limits based on the selected range
    ax.set_xlim(sorted_indices[window_pos[0]], sorted_indices[window_pos[0] + window_size - 1])

    # Update x-axis ticks and labels
    x_ticks_interval = max(1, window_size // 20)
    ax.set_xticks(sorted_indices[window_pos[0]:window_pos[0] + window_size:x_ticks_interval])
    ax.set_xticklabels(df['Date'].iloc[sorted_indices[window_pos[0]:window_pos[0] + window_size:x_ticks_interval]], rotation=45, ha='right')

    # Update the data
    line.set_xdata(sorted_indices[window_pos[0]:window_pos[0] + window_size])
    line.set_ydata(sorted_close.iloc[window_pos[0]:window_pos[0] + window_size])

    # Update y-axis limits with a margin
    ax.set_ylim(sorted_close.iloc[window_pos[0]:window_pos[0] + window_size].min() - 1000,
                sorted_high.iloc[window_pos[0]:window_pos[0] + window_size].max() + 1000)

    # Redraw the canvas
    fig.canvas.draw_idle()

# Connect the slider to the update function
slider_range.on_changed(update)

# Show the dynamic plot
plt.show()
