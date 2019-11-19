from flask import Flask
from flask import jsonify

from selenium import webdriver
driver = webdriver.Firefox()
website = "https://www.imdb.com"
driver.get(website)
driver.close()

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