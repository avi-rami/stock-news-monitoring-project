import requests
from twilio.rest import Client

# Define constants
STOCK = "TSLA"  # Stock symbol for Tesla
COMPANY_NAME = "Tesla Inc"  # Company name for news search
STOCK_API_KEY = "M8C9ZX4NQBFPNIYZ"  # API key for Alpha Vantage (for stock data)
NEWS_API_KEY = "23e06b8822ff481cb53cadfd1a7bc97a"  # API key for NewsAPI (for news articles)

# Twilio API credentials
account_sid = "ACea318315eb262b02f5f78a9ffbe85244"
auth_token = "a1644bc3e5cbcf24392c0bbab5f1f4f3"
client = Client(account_sid, auth_token)  # Initialize Twilio client

# Get stock data (daily time series) from Alpha Vantage
# The below two lines are for actual API use, currently commented out to avoid daily token usage
# url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={STOCK_API_KEY}'
# r = requests.get(url)

# Example with demo data (for IBM stock)
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
r = requests.get(url)
stock_data = r.json()["Time Series (Daily)"]  # Extract daily time series data

# Calculate closing prices for the last two days
closing_prices = []
for date in sorted(stock_data)[-2:]:
    closing_price = stock_data[date]["4. close"]
    closing_prices.append(float(closing_price))

today_closing_price = closing_prices[0]  # Most recent closing price
yesterday_closing_price = closing_prices[1]  # Previous day's closing price

# Calculate the price difference and percentage change
price_difference = abs(yesterday_closing_price - today_closing_price)
percent_difference = round((price_difference / yesterday_closing_price) * 100, 2)

# Initialize flags for stock increase/decrease
stock_increased = False
stock_decreased = False

# Determine if the stock has increased or decreased by 5% or more
if percent_difference >= .5:  # Adjusted to 5% from 0.5%
    stock_increased = True
    message_symbol = "🔺"  # Symbol for increase
elif percent_difference <= -.5:  # Adjusted to -5% from -0.5%
    stock_decreased = True
    message_symbol = "🔻"  # Symbol for decrease

# Get news articles for the company from NewsAPI
url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey={NEWS_API_KEY}"
r = requests.get(url)
news_data = r.json()["articles"]  # Extract articles from the response

# If stock increased or decreased by 5% or more, send SMS notifications
if stock_increased or stock_decreased:
    for article in news_data[:3]:  # Get the first 3 news articles
        # Construct the message with stock change, headline, and brief
        message = client.messages.create(
            body=f"TSLA: {message_symbol}{percent_difference}%\nHeadline: {article['title']}\nBrief: {article['description']}",
            from_="whatsapp:+14155238886",  # Twilio sandbox WhatsApp number
            to="whatsapp:+19515003278",  # Your phone number on WhatsApp
        )
