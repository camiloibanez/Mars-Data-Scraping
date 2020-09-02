def scrape():
    from bs4 import BeautifulSoup
    from splinter import Browser
    import pandas as pd
    import datetime
    import time
    import os
    import sys
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC


    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    chrome_options = Options()
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    # driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)

    # Scraping latest mars news
    url = "https://mars.nasa.gov/news/"
    driver.get(url)
    
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Scraping latest features image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    image_url = soup.find_all('article', class_='carousel_item')[0]['style'][24:-3]
    featured_image_url = 'https://www.jpl.nasa.gov/' + image_url

    # Scraping latest mars weather
    url = "https://twitter.com/marswxreport?lang=en"
    driver.get(url)

    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
    # time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.article.find_all('span')[4].text

    sys.stderr.write("I made it past twitter")
    
    driver.quit()
    
    # Recorded time of scrape
    last_scraped = datetime.datetime.now()
    last_scraped = last_scraped.strftime("%Y-%m-%d %I:%M")
    last_scraped = last_scraped.replace(" 0", " ")

    results = {"news_title": news_title, "news_p": news_p, "featured_image_url" : featured_image_url, "mars_weather": mars_weather,
        "last_scraped": last_scraped}
    
    return results