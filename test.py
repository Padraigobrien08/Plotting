import pandas as pd
from matplotlib.widgets import RangeSlider, CheckButtons
import matplotlib.pyplot as plt

# Read the CSV data
df = pd.read_csv("BTC-USD.csv")

# Create a new figure for the dynamic plot
fig, ax = plt.subplots(figsize=(15, 8))

# Initial window size and position
initial_window_size = 100
initial_window_pos = 0

# Plot all lines for the initial window
line_close, = ax.plot(df['Date'][initial_window_pos:initial_window_pos + initial_window_size],
                      df['Close'][initial_window_pos:initial_window_pos + initial_window_size],
                      label='Closing Value', linestyle='-', alpha=1.0)

line_high, = ax.plot(df['Date'][initial_window_pos:initial_window_pos + initial_window_size],
                     df['High'][initial_window_pos:initial_window_pos + initial_window_size],
                     label='High Value', linestyle='-', alpha=1.0)

line_low, = ax.plot(df['Date'][initial_window_pos:initial_window_pos + initial_window_size],
                    df['Low'][initial_window_pos:initial_window_pos + initial_window_size],
                    label='Low Value', linestyle='-', alpha=1.0)

line_open, = ax.plot(df['Date'][initial_window_pos:initial_window_pos + initial_window_size],
                     df['Open'][initial_window_pos:initial_window_pos + initial_window_size],
                     label='Open Value', linestyle='-', alpha=1.0)

# Customize the plot
ax.set_title('Bitcoin Price Over Time')
x_ticks_interval = max(1, initial_window_size // 20)
ax.set_xticks(df.index[initial_window_pos:initial_window_pos + initial_window_size:x_ticks_interval])
ax.set_xticklabels(df['Date'].iloc[df.index[initial_window_pos:initial_window_pos + initial_window_size:x_ticks_interval]], rotation=45, ha='right')
ax.grid(True)
ax.set_ylabel('Price')
ax.set_position([0.05,0.15,0.93, 0.8])
ax.legend()

# Add a RangeSlider with two thumbs for selecting the window
ax_slider_range = plt.axes([0.1, 0, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider_range = RangeSlider(ax_slider_range, 'Show N Dates', valmin=1, valmax=len(df['Date']),
                           valinit=[initial_window_pos, initial_window_pos + initial_window_size], valstep=1)

# Add CheckButtons to toggle visibility of lines
ax_check = plt.axes([0.9, 0.2, 0.1, 0.15], facecolor='lightgoldenrodyellow')
check_buttons = CheckButtons(ax_check, labels=['Close', 'High', 'Low', 'Open'], actives=[True, True, True, True])


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
    sorted_low = df['Low'].iloc[sorted_indices]
    sorted_open = df['Open'].iloc[sorted_indices]

    # Update x-axis limits based on the selected range
    ax.set_xlim(sorted_indices[window_pos[0]], sorted_indices[window_pos[0] + window_size - 1])

    # Update x-axis ticks and labels
    x_ticks_interval = max(1, window_size // 20)
    ax.set_xticks(sorted_indices[window_pos[0]:window_pos[0] + window_size:x_ticks_interval])
    ax.set_xticklabels(df['Date'].iloc[sorted_indices[window_pos[0]:window_pos[0] + window_size:x_ticks_interval]], rotation=45, ha='right')

    # Update the data
    line_close.set_xdata(sorted_indices[window_pos[0]:window_pos[0] + window_size])
    line_close.set_ydata(sorted_close.iloc[window_pos[0]:window_pos[0] + window_size])
    line_high.set_xdata(sorted_indices[window_pos[0]:window_pos[0] + window_size])
    line_high.set_ydata(sorted_high.iloc[window_pos[0]:window_pos[0] + window_size])
    line_low.set_xdata(sorted_indices[window_pos[0]:window_pos[0] + window_size])
    line_low.set_ydata(sorted_low.iloc[window_pos[0]:window_pos[0] + window_size])
    line_open.set_xdata(sorted_indices[window_pos[0]:window_pos[0] + window_size])
    line_open.set_ydata(sorted_open.iloc[window_pos[0]:window_pos[0] + window_size])

    # Update y-axis limits with a margin
    ax.set_ylim(sorted_close.iloc[window_pos[0]:window_pos[0] + window_size].min() - 1000,
                sorted_high.iloc[window_pos[0]:window_pos[0] + window_size].max() + 1000)

    # Redraw the canvas
    fig.canvas.draw_idle()


# Connect the slider to the update function
slider_range.on_changed(update)


# Checkbox update function
def update_visibility(label):
    lines = {'Close': line_close, 'High': line_high, 'Low': line_low, 'Open': line_open}
    lines[label].set_alpha(1.0 if lines[label].get_alpha() == 0 else 0.0)

    # Update legend
    handles, labels = ax.get_legend_handles_labels()
    updated_handles = []
    updated_labels = []

    for handle, lbl in zip(handles, labels):
        if lines.get(lbl, None) is not None and lines[lbl].get_alpha() != 0:
            updated_handles.append(handle)
            updated_labels.append(lbl)

    fig.canvas.draw_idle()


check_buttons.on_clicked(update_visibility)

# Show the dynamic plot
plt.show()
