import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.who.int/news-room'

headers = {

    'User-Agent':
    'Mozilla/5.0'
}

response = requests.get(
    url,
    headers=headers
)

soup = BeautifulSoup(
    response.text,
    'html.parser'
)

headlines = []

cards = soup.find_all('a')[:50]

for card in cards:

    text = card.get_text(strip=True)

    if len(text) > 40:

        headlines.append(text)

health_df = pd.DataFrame({

    'headline': headlines[:10]
})

health_df.to_csv(
    'data/health_alerts.csv',
    index=False
)

print("Health alerts scraped successfully")
print(health_df.head())