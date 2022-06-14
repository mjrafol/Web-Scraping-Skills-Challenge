# Automates browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd
import time
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

# Defining a function to scrape mars data
def scrape():

    # Set-up connection to mongodb
    # create a connection screen
    conn = 'mongodb://localhost:27017'

    # pass connection to pymongo instance
    client = pymongo.MongoClient(conn)

    # connect to a database
    db = client.mars_app

    # drop collection if available to remove duplicates
    db.mars_data.drop()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # *********************************************************************************
    # SCRAPE THE LATEST MARS NEWS
    # *********************************************************************************
 
    # The url we want to scrape
    url_news = 'https://redplanetscience.com/'

    # Print text to commence the scrape
    print("Scraping the latest news...")
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url_news)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the content title and article teaser body
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    # # Store data in a dictionary --> moved to the end
    # mars_data = {
    #     "news_title": news_title,
    #     "news_p": news_p
    # }

    # Quit the browser
    browser.quit()

    # Print text to complete the scrape
    print("Scraping the latest news completed.")


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # *********************************************************************************
    # SCRAPE THE MARS FACTS
    # *********************************************************************************

    # The url we want to scrape
    url_facts = 'https://galaxyfacts-mars.com'

    # Print text to commence the scrape
    print("Scraping the mars facts...")

    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url_facts)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the table
    dfs = pd.read_html(url_facts)
    table_1 = dfs[0]
    mars_facts = table_1.rename(columns={0 : "Description",
                                    1 : "Mars",
                                    2 : "Earth"})

    html_table = mars_facts.to_html(index=False, header=False, border=0, classes="table table-sm table-striped font-weight-light")

    # # Store data in a dictionary --> moved to the end
    # mars_data = {
    #     "mars_facts": html_table
    # }

    # # Quit the browser
    # browser.quit()

    # Print text to complete the scrape
    print("Scraping the mars facts completed.")

    # *********************************************************************************
    # SCRAPE THE FEATURED IMAGE URL
    # *********************************************************************************

    # The url we want to scrape
    url_image = 'https://spaceimages-mars.com'
    
    # Print text to commence the scrape
    print("Scraping the featured image...")

    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url_image)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the image url
    image = soup.find('img', class_='headerimage')
    image_file = image.get('src')
    featured_image_url = url_image + "/" + image_file

    # # Store data in a dictionary --> moved to the end
    # mars_data = {
    #     "featured_image_url": featured_image_url
    # }

    # # Quit the browser
    # browser.quit()

    # Print text to complete the scrape
    print("Scraping the featured image completed.")


    # *********************************************************************************
    # SCRAPE THE MARS HEMISPHERES
    # *********************************************************************************

    # The url we want to scrape
    url_hem = 'https://marshemispheres.com/'

    # Print text to commence the scrape
    print("Scraping the mars hemispheres...")

    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url_hem)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")
    hemispheres = soup.find_all('div', class_='description')

    # Create an empty list to store the dictionary
    hemisphere_image_urls = []

    # looping through the hemispheres
    for hemisphere in hemispheres:
        
        # Identify and return the title
        title = hemisphere.find('h3').text
        
        # Identify and return the link
        link = hemisphere.a['href']
        url_link = url_hem + link
               
        # Visit the website
        browser.visit(url_link)
        
        # Grab the html    
        html = browser.html
        
        # Create BeautifulSoup object and parse with 'html.parser'
        each = BeautifulSoup(html, 'html.parser')
        
        # Scrape the content of class "wide-image"
        each_class = each.find('div', class_='downloads')
        link = each_class.a['href']
        image_url = url_hem + link
        
        # Create a dictionary to store data using the keys img_url and title
        hem_dict = ({"title": title, "img_url" : image_url})
        hemisphere_image_urls.append(hem_dict)

    # Quit the browser
    browser.quit()

    # Check if the script ran
    print("Scraping the mars hemispheres completed.")

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,

        "mars_facts": html_table,

        "featured_image_url": featured_image_url,

        "title_card1": hemisphere_image_urls[0]['title'],
        "image_card1": hemisphere_image_urls[0]['img_url'],

        "title_card2": hemisphere_image_urls[1]['title'],
        "image_card2": hemisphere_image_urls[1]['img_url'],

        "title_card3": hemisphere_image_urls[2]['title'],
        "image_card3": hemisphere_image_urls[2]['img_url'],
 
        "title_card4": hemisphere_image_urls[3]['title'],
        "image_card4": hemisphere_image_urls[3]['img_url'],
    }    

    # Return our dictionary
    return mars_data



