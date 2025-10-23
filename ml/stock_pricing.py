# pip install requests matplotlib


import requests
import matplotlib.pyplot as plt
from collections import deque
import time

# Use a public API for real data, e.g., Finnhub.io or Alpha Vantage.
# This example uses a placeholder URL and dummy data.
def get_stock_price(ticker):
    """Fetches real-time stock price from a mock API."""
    # Replace this with a real API call.
    # Example using dummy data:
    if ticker == 'AAPL':
        # Simulate a slight price fluctuation
        return 150.0 + (time.time() % 10) * 0.5 - 2.5
    else:
        return None

def main():
    """Fetches and plots stock prices in real time."""
    stock_ticker = 'AAPL'
    time_series_data = deque(maxlen=50) # Use a deque for efficient sliding window
    time_points = deque(maxlen=50)

    plt.ion() # Turn on interactive mode
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'o-')
    ax.set_title(f"Real-Time Stock Price for {stock_ticker}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Price ($)")

    start_time = time.time()

    try:
        while True:
          #code by Madhav :)
            current_price = get_stock_price(stock_ticker)
            if current_price is not None:
                current_time = time.time() - start_time
                time_series_data.append(current_price)
                time_points.append(current_time)

                # Update plot data
                line.set_xdata(time_points)
                line.set_ydata(time_series_data)

                # Adjust plot limits dynamically
                ax.relim()
                ax.autoscale_view()

                # Redraw the plot
                fig.canvas.draw()
                fig.canvas.flush_events()

            time.sleep(1) # Update every second

    except KeyboardInterrupt:
        print("\nStopping real-time plot.")
        plt.ioff()
        plt.show()
