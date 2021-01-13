from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape():

    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Get Featured Mars News
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    time.sleep(2)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.findAll("div",{"class": "content_title"})
    news_title = news_title[1].text

    time.sleep(2)

    news_p = soup.find("div",{"class": "article_teaser_body"}).text

    #Get Featured Image

    # Build the main connection and create HTML Object
    mars_news_url = 'https://www.jpl.nasa.gov/images/?search=&category=Mars'
    browser.visit(mars_news_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the HTML for the featured image first on list
    featured_image_url = soup.find("div",{"class": "sm:object-cover object-cover"})
    featured_image_url = f"{featured_image_url.find('img')['src'][0:57]}.width-1600.jpg"

    #Get Mars Facts

    # Store url in variable
    mars_facts = 'https://space-facts.com/mars/'

    # Use panda to read HTML contents
    raw_html_table = pd.read_html(mars_facts)

    # Select the first intance of a table
    mars_facts_df = raw_html_table[0]
    mars_facts_df.columns =['Description', 'Value']

    # Convert newly created Mars facts table back
    mars_facts = mars_facts_df.to_html(index=False).replace('\n','')

    # Build the main connection and create HTML Object
    mars_hemisphere_img_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_img_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #-----------------------------------------------------------------
    # get all the info that contains the image links
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Go through all links and retreive images
    for ele in items: 
        # Get title on intial page
        title = ele.find('h3').text
    
        # Find and Store url to img
        img_url = ele.a['href']
    
        # Go To new page
        browser.visit(hemispheres_main_url + img_url)
    
        # New HTML Object to traverse
        partial_img_html = browser.html
    
        # Find the site
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
        # getting full image url 
        img_url = soup.find('li').a['href']
    
        # Adding to dictionary
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

    # Store all gathered data into a dictionatary
    mars_data={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_fact_table":mars_facts,
        "hemisphere_images":hemisphere_image_urls
    }

    # Close browser and return dictionary
    browser.quit()
    return mars_data
scrape()