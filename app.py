from flask import Flask, render_template, redirect
import pymongo

app = Flask(__name__)

conn = "mongodb+srv://Client1:QEPI88Emag3yxyvU@mars-scraped-info.0hpmq.mongodb.net/mars_db?retryWrites=true&w=majority"
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

    results = scrape()

    db.scraped_info.drop()
    db.scraped_info.insert_one(
        results
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)