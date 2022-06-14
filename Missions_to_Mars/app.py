from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo

# importing our scrape_mars script
import scrape_mars

# create an instance of Flask
app = Flask(__name__)

# # use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')
mars_data = mongo.db.mars_data

# create a home route
@app.route("/")

# create a function
def home():

    # # find one document from our mongo db and return it.
    mars_data = mongo.db.mars_data.find_one()

    # pass that listing to render_template
    return render_template("index.html", mars_data=mars_data)

# set our path to /scrape
@app.route("/scrape")

# define a function
def scraper():

    # create a database
    mars_data = mongo.db.mars_data

    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    scraped_data = scrape_mars.scrape()

    # insert our listings with the data that is being scraped.
    mars_data.insert_one(scraped_data)

    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
