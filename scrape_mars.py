from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
import re



# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     return Browser("chrome", **executable_path, headless=False)


# def scrape():
#     browser = init_browser()
#     listings = {}

#     url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
#     browser.visit(url)

#     html = browser.html
#     soup = BeautifulSoup(html, "html.parser")

#     listings["headline"] = soup.find("a", class_="result-title").get_text()
#     listings["price"] = soup.find("span", class_="result-price").get_text()
#     listings["hood"] = soup.find("span", class_="result-hood").get_text()

#     return listings

def scrape():
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph=mars_news(browser)
    
    # data={}
    # data["news_title"]=news_title,
    # data["news_paragraph"]=news_paragraph,
    # data["featured_image"]=featured_image(browser),
    # data["hemisphere"]=hemisphere(browser),
    # data["weather"]=weather(browser),
    # data["facts"]=facts(browser),
    # data["last_modified"]=dt.datetime.now()
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemisphere(browser),
        "weather": weather(browser),
        "facts": facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
    url="https://mars.nasa.gov/news/"
    browser.visit(url)

    #get first element and wait 0.5s if not present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html=browser.html
    news_soup=BeautifulSoup(html, "html.parser")

    try:
        slide_elem=news_soup.select_one("ul.item_list li.slide")
        news_title=slide_elem.find("div",class_="content_title").get_text()
        news_p=slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


def featured_image(browser):
    mars_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html_mars=browser.html
    img_soup=BeautifulSoup(html_mars,"html.parser")

    try:
        img_url=img_soup.find_all('img')[3]["src"]
        main_url="https://www.jpl.nasa.gov"
        featured_image_url=main_url+img_url
        #featured_image_url.click()
    except AttributeError:
        return None
    return featured_image_url

def hemisphere(browser):
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')

    try:
        base_url='https://astrogeology.usgs.gov'
        items=hemispheres_soup.find_all('div',class_="item")
        imge_urls=[]
        for i in items:
            title=i.find('h3').text
            partial_img_url=i.find('a',class_='itemLink product-item')['href']
            browser.visit(base_url+partial_img_url)
            partial_img_html=browser.html
            img_soup=BeautifulSoup(partial_img_html, "html.parser")
            img_url=base_url+img_soup.find('img',class_="wide-image")['src']
            imge_urls.append({'title':title,"imagr_url":img_url})
    except AttributeError:
        return None
    return imge_urls


def weather(browser):
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    try:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find('span', text=pattern).get_text()
    except AttributeError:
        return None
    return mars_weather

def facts():
    facts_url = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(facts_url)
    mars_facts_df = mars_tables[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_html_table=mars_facts_df.to_html()
    return mars_html_table








