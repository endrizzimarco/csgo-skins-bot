from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options 
import time

def parseListing(href):
  options = webdriver.ChromeOptions()
  options.add_extension('./extension_1_17_60_0.crx')
  driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
  driver.get(href)

  wait = WebDriverWait(driver, 10)
  delay = 10  # seconds
  data = {}
  currentPage = 1

  try:
    # Have to go to page 2 and back to 1 to fix steam shitty bug
    driver.find_element_by_xpath("//span[@id='searchResults_links']/span[2]").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//span[@id='searchResults_links']/span[1]").click()
    

    while True:
      WebDriverWait(driver, delay).until(
      EC.presence_of_element_located((By.ID, 'allfloatbutton'))
      )
      time.sleep(1)
      # Click extension's buttons to show float values
      driver.find_element_by_id("allfloatbutton").click()
      if currentPage == 1:
        driver.find_element_by_id("sortlistings").click()
      
      time.sleep(1) # Wait a sec to load float values
      listing = driver.find_elements_by_class_name('market_recent_listing_row') # DUMP IT

      # Fetch data for every item on this page
      for item in listing:
        itemId = item.get_attribute('id').split('_')[1]
        price = item.find_element_by_class_name('market_listing_price_with_fee').text
        floatValue = item.find_element_by_class_name('itemfloat').find_element_by_class_name('value').text
        data[itemId] = [price, floatValue]
      
      # Check whether to go next page or not
      currentPage += 1
      if not driver.find_element_by_xpath(f"//span[@id='searchResults_links']/span[{currentPage}]") or currentPage > 5:
        break
      time.sleep(4)
      driver.find_element_by_xpath(f"//span[@id='searchResults_links']/span[{currentPage}]").click()

  except TimeoutException:
    print('Loading took too much time!')

  finally:
    driver.quit()
    return data
