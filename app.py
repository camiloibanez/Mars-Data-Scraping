from flask import Flask, render_template, redirect
import pymongo

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

@app.route("/")
def index():

    results = db.scraped_info.find_one()

    pic1 = results['hemisphere_image_urls'][0]
    pic2 = results['hemisphere_image_urls'][1]
    pic3 = results['hemisphere_image_urls'][2]
    pic4 = results['hemisphere_image_urls'][3]

    tables = [results['Mars_facts_table']]

    return render_template('index.html', dict=results, pic1=pic1, pic2=pic2, pic3=pic3, pic4=pic4, tables=tables)

@app.route("/scrape")
def to_scrape():
    from scrape_mars import scrape

    db.scraped_info.drop()
    db.scraped_info.insert_one(
        scrape()
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)