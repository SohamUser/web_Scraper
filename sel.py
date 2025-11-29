import requests
from bs4 import BeautifulSoup

def scrape_steam_game(url: str):
    headers = {
        "User-Agent": (
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }

    cookies = {
        'birthtime': '568022401',
        'lastagecheckage': '1-0-1988',
        'wants_mature_content': '1'
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    name_tag = soup.find('div', id='appHubAppName')
    img_tag = soup.find('img', class_='game_header_image_full')
    price_tag = soup.find('div', class_='discount_final_price') or soup.find('div', class_='game_purchase_price')
    description_tag = soup.find('div', class_='game_description_snippet')
    release_tag = soup.find('div', class_='release_date')

    description = description_tag.text.strip() if description_tag else "No description"
    release_date = release_tag.find('div', class_='date').text.strip() if release_tag else "Unknown"

    return {
        "name": name_tag.text.strip() if name_tag else "Not found",
        "image": img_tag['src'] if img_tag else "Not found",
        "price": price_tag.text.strip() if price_tag else "Not found",
        "platform": "Steam",
        "url": url,
        "description": description,
        "release_date": release_date
    }
