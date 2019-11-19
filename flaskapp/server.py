from flask import Flask
from flask import jsonify

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
website = "https://www.imdb.com"
driver.get(website)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def display():
    return "Looks like it works!"

@app.route('/show=<show>', methods=['POST', 'GET'])
def addShow(show):
    print(show)
    return jsonify([show, "here", "lol"])

if __name__=='__main__':
    app.run(host="0.0.0.0", port="80")