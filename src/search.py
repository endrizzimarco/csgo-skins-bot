from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.select import Select
import configparser

def search():
  config = configparser.ConfigParser()
  config.read('config.ini')
  config = config['DEFAULT']

  collection = config['COLLECTION']
  exterior = config['EXTERIOR']
  category = config['CATEGORY']
  quality = config['QUALITY']
  depth = int(config['DEPTH'])

  data = []
  selector = 'a.btn_small.btn_grey_white_innerfade'
  delay = 10  # seconds

  driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
  driver.get('https://steamcommunity.com/market/search?appid=730')

  try:
    # Wait for data to be loaded
    WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.market_search_advanced_button'))
    )

    # Open advanced menu option
    driver.find_element_by_css_selector("div.market_search_advanced_button").click()

    if (collection):
      # Select collection
      try:
        objSelect = Select(driver.find_element_by_name("category_730_ItemSet[]"))
        objSelect.select_by_visible_text(collection);
      except NoSuchElementException:
        print(f'There is no collection named {collection}')
        driver.quit()

    if (exterior):
      # Select weapon exterior
      try:
        exteriorOpts = {'Field-Tested': 'tag_730_Exterior_WearCategory2', 'Minimal Wear': 'tag_730_Exterior_WearCategory1'}
        driver.find_element_by_id(exteriorOpts[exterior]).click()
      except KeyError:
        print(f'There is no exterior named {exterior}')
        driver.quit()

    if (category):
      # Select category
      try:
        categoryOpts = {'Normal': 'tag_730_Quality_normal', 'StatTrak': 'tag_730_Quality_strange'}
        driver.find_element_by_id(categoryOpts[category]).click()
      except KeyError:
        print(f'There is no category named {category}')
        driver.quit()

    if (quality):
      # Select quality
      try:
        qualityOpts = {'Restricted': 'tag_730_Rarity_Rarity_Mythical_Weapon', 'Classified': 'tag_730_Rarity_Rarity_Legendary_Weapon'}
        driver.find_element_by_id(qualityOpts[quality]).click()
      except KeyError:
        print(f'There is no quality named {quality}')
        driver.quit()

    # Submit search
    driver.find_element_by_css_selector("div.btn_medium.btn_green_white_innerfade").click()


    listing = driver.find_elements_by_class_name('market_listing_row_link')

    for item in listing[:depth]:
      data.append(item.get_attribute('href'))

  except TimeoutException:
    print('Loading took too much time!')

  finally:
    driver.quit()
    return data