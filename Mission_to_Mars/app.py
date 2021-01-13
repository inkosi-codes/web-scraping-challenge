from flask import Flask, render_template, redirect, jsonify
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = mongo["marsdb"]
mars_col = mydb["mars_info"]

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    mars_data = mars_col.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()

    mars_col.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)