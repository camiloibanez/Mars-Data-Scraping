def scrape():
    from bs4 import BeautifulSoup
    from splinter import Browser
    import pandas as pd
    import datetime
    import time

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_url = soup.find_all('article', class_='carousel_item')[0]['style'][24:-3]
    featured_image_url = 'https://www.jpl.nasa.gov/' + image_url

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.article.find_all('span')[4].text

    Mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    Mars_facts_df.rename(columns={0: "description", 1: "value"}, inplace=True)
    Mars_facts_df.set_index(['description', 'value'], inplace=True)
    Mars_facts_table = Mars_facts_df.to_html(classes='data', header=True)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    for peice in soup.find_all('div', class_="description"):
        title_list = peice.h3.text.split(" ")
        title_list.pop()
        title = " ".join(title_list)
        hemisphere_image_urls.append({'title': f"{title}"})
    
    for x in range(len(hemisphere_image_urls)):
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.click_link_by_partial_text(f"{hemisphere_image_urls[x]['title']}")
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_image_urls[x]['img_url'] = soup.find('div', class_="downloads").find_all('a')[0]['href']

    browser.quit()
    
    last_scraped = datetime.datetime.now()
    last_scraped = last_scraped.strftime("%Y-%m-%d %I:%M")

    results = {"news_title": news_title, "news_p": news_p, "featured_image_url" : featured_image_url, "mars_weather": mars_weather,
        "Mars_facts_table" : Mars_facts_table, "hemisphere_image_urls": hemisphere_image_urls, "last_scraped": last_scraped}
    
    return results