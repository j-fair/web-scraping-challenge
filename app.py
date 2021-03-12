from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Firing up mongodb
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_dict = mongo.db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mars_dict.update({}, mars_data, upsert=True)
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)