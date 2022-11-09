# Importing necessary libraries.
from flask import Flask, json, render_template, request, flash
import requests
import json
import random

# Defining Flask app.
app = Flask(__name__)
def get_country_data():
    response=requests.get("https://countriesnow.space/api/v0.1/countries/capital", verify=False)
    country_data = dict()
    countriesnow = json.loads(response.text)["data"]
    for country in countriesnow:
        country_data[country["name"]] = country["capital"]
    return country_data
# Main page
@app.route('/')
def home():
    country_data = get_country_data()
    random_country = random.choice(list(country_data.keys()))
    with open("temp.json", "w+") as fp:
        json.dump({"country": random_country}, fp)
    return render_template('index.html', random_country=random_country)

@app.route('/refresh', methods=["GET"])
def refresh():
    country_data = get_country_data()
    random_country = random.choice(list(country_data.keys()))
    with open("temp.json", "w+") as fp:
        json.dump({"country": random_country}, fp)
    return render_template('index.html', random_country=random_country)

# Check API
@app.route("/check", methods=["POST", "GET"])
def check():
    if request.method == 'POST':
        country_data = get_country_data()
        capital_name = request.form["capital"]
        with open("temp.json", "r") as fp:
            country = json.load(fp)
        country = country["country"]
        if country_data[country].lower() == capital_name.lower():
            flash('Great! You have entered right capital of {}.'.format(country))
        else:
            flash("Oops! That's wrong. The correct capital of {} is {}".format(country, country_data[country]))
        return render_template('index.html', random_country=country)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
