

from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    mars_facts_data = {}

    url_nasa = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa)

    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    #scrapping latest news about mars from nasa
    # save the most recent article, title and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_p 
    mars_facts_data['date']=news_date
    
    #Mars Featured Image
    url_img = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)

    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html_img = browser.html
    soup = BeautifulSoup(html_img, 'html.parser')
    img_url = soup.find("img", class_="thumb")["src"]
    full_img_url = "https://jpl.nasa.gov"+img_url
    mars_facts_data["featured_image"] = full_img_url
    
    # #### Mars Weather
    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_facts_data["mars_weather"] = mars_weather

    # #### Mars Facts

    url_facts = "https://space-facts.com/mars/"
    mars_fact = pd.read_html(url_facts)
    mars_fact_df = mars_fact[0]
    mars_fact_df.columns = ["Parameter", "Values"]
    mars_fact_df.set_index(["Parameter"])
    mars_html_table = mars_fact_df.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html_table

    # #### Mars Hemisperes

    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    html_hemis = browser.html
    soup = BeautifulSoup(html_hemis, 'html.parser')
    mars_hemis=[]

    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    mars_facts_data["hemisphere_img_url"] = mars_hemis

    #print(mars_facts_data)
    return mars_facts_data






