import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.who.int/news-room"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

headlines = []

news_cards = soup.find_all(
    ["h2", "h3", "h4"]
)

for card in news_cards:

    text = card.get_text(strip=True)

    if len(text) > 25:

        headlines.append(text)

headlines = list(dict.fromkeys(headlines))

health_df = pd.DataFrame({

    "headline": headlines[:15]
})

health_df.to_csv(
    "data/health_alerts.csv",
    index=False
)

print("Health alerts updated successfully")
print(health_df.head())