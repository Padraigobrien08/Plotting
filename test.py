# Because the jupyter notebooks arent committing to git nicely
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

# Read the CSV data
df = pd.read_csv("BTC-USD.csv")

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03)

# Add traces for each line
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Closing Value'), row=1, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['High'], mode='lines', name='High Value'), row=1, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'], mode='lines', name='Low Value'), row=1, col=1)
fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], mode='lines', name='Open Value'), row=1, col=1)

# Update layout with larger size
fig.update_layout(
    title='Bitcoin Price Over Time',
    xaxis=dict(title='Date', tickangle=45),
    yaxis=dict(title='Price'),
    showlegend=True,
    height=1200,  # Adjust the height as needed
    width=1200   # Adjust the width as needed
)

# Show the Plotly plot
fig.show()