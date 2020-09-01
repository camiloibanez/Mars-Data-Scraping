def scrape():
    from bs4 import BeautifulSoup
    from splinter import Browser
    import pandas as pd
    import datetime
    import time
    import os
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    chrome_options = Options()
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

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

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.article.find_all('span')[4].text

    # Scraping mars quick facts
    Mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    Mars_facts_df.rename(columns={0: "description", 1: "value"}, inplace=True)
    Mars_facts_df.set_index(['description', 'value'], inplace=True)
    Mars_facts_table = Mars_facts_df.to_html(classes='data', header=True)

    # Scraping images of mars hemispheres and their titles
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    
    # Scraping mars hemisphere titles
    for piece in soup.find_all('div', class_="description"):
        title_list = piece.h3.text.split(" ")
        title_list.pop()
        title = " ".join(title_list)
        hemisphere_image_urls.append({'title': f"{title}"})
    
    # Scraping mars hemisphere images
    for x in range(len(hemisphere_image_urls)):
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.click_link_by_partial_text(f"{hemisphere_image_urls[x]['title']}")
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_image_urls[x]['img_url'] = soup.find('div', class_="downloads").find_all('a')[0]['href']

    driver.quit()
    
    # Recorded time of scrape
    last_scraped = datetime.datetime.now()
    last_scraped = last_scraped.strftime("%Y-%m-%d %I:%M")
    last_scraped = last_scraped.replace(" 0", " ")

    results = {"news_title": news_title, "news_p": news_p, "featured_image_url" : featured_image_url, "mars_weather": mars_weather,
        "Mars_facts_table" : Mars_facts_table, "hemisphere_image_urls": hemisphere_image_urls, "last_scraped": last_scraped}
    
    return results