from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def getInspectLink(url):
    html = None
    selector = 'a.btn_small.btn_grey_white_innerfade'
    delay = 10  # seconds
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)

    try:
        # wait for data to be loaded
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        print('Loading took too much time!')
    else:
        html = browser.page_source
    finally:
        browser.quit()

    if html:
        soup = BeautifulSoup(html, features='html.parser')
        inspectLink = soup.select_one(selector)['href']
        return inspectLink


link = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Knife&appid=730#p1_price_asc'
page = urlopen(link)

bs_page = BeautifulSoup(page.read(), features="html.parser")
objects = bs_page.findAll(class_="market_listing_row_link")
data = []


for obj in objects:
    link  = obj["href"]
    price = obj.find('span', {'data-price': True})['data-price']
    price = int(price)
    data.append((price, link, getInspectLink(link)))

data = sorted(data)

print("\n".join(f"${price/100} USD | {floatValue} | {link}" for price, link, floatValue in data))