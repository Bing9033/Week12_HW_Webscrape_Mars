#!/usr/bin/env python
# coding: utf-8

# In[4]:


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import time

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


@app.route("/")
def home():
    mars = mongo.db.mars.find()
    time.sleep(2)
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({},mars_data,upsert=True)
    time.sleep(3)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)



