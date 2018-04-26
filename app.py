# Dependencies
from flask import Flask, render_template, jsonify, redirect, request
from scrape_yelp import search_yelp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('yelp.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    search = request.form['search']
    search_zipcode = request.form['zipcode']
    
    search_yelp(search, search_zipcode)
    # yelp_data = scrape_yelp.scrape()


    return redirect("/", code=302)




if __name__ == "__main__":
    app.run(debug=True)