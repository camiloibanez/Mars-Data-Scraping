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
    from scrape_mars_heroku import scrape

    results = scrape()

    results2 = {'Mars_facts_table': '<table border="1" class="dataframe data">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th></th>\n    </tr>\n    <tr>\n      <th>description</th>\n      <th>value</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <th>6,792 km</th>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <th>6,752 km</th>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <th>6.39 × 10^23 kg (0.11 Earths)</th>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <th>2 (Phobos &amp; Deimos)</th>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <th>227,943,824 km (1.38 AU)</th>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <th>687 days (1.9 years)</th>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <th>-87 to -5 °C</th>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <th>2nd millennium BC</th>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <th>Egyptian astronomers</th>\n    </tr>\n  </tbody>\n</table>', 'hemisphere_image_urls': [{'title': 'Cerberus Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}

    results.update(results2)

    print(results)

    db.scraped_info.drop()
    db.scraped_info.insert_one(
        results
    )
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)