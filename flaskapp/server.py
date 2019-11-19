from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import requests
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import glob
import os
from os import path
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
app = Flask(__name__)
#app.run(debug=True)

def strip(tags):
    new_tags = []
    for tag in tags:
        re.sub("<.*?>", "", tag)
        new_tags.append(tag)
    return new_tags


class WebScraper:
    def __init__(self):
        self.shows = {}
        self.stemmer = nltk.stem.SnowballStemmer('english')
        print("started")
        
    def model(self):
        if self.show_url in self.shows:
            print("found the show!")
            return self.shows[self.show_url]
        txt = self.summary
        txt = (re.split(r'\W+', txt))
        txt = " ".join([self.stemmer.stem(word) for word in txt])
        vect = TfidfVectorizer(stop_words = 'english')
        tfidf_matrix = vect.fit_transform([txt, " ".join([word for word in self.content])])
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=vect.get_feature_names())
        cp = df.iloc[0].sort_values(inplace=False, ascending=False)
        self.cp = cp
        self.shows[self.show_url] = list(cp[0:10].keys())
        return list(cp[0:10].keys())
        
    def get_list(self):
        return self.cp

    def scrape(self, show):
        options = Options()
        self.show = show
        options.headless = True
        driver = webdriver.Firefox(options=options)
        website = "https://www.imdb.com"
        driver.get(website)
        search = driver.find_element_by_name("q")
        search.send_keys(show)
        search_button = driver.find_element_by_id('navbar-submit-button')

        search_button.click()

        result = requests.get(driver.current_url)
        soup = BeautifulSoup(result.content)
        po = (soup.find_all('table', class_='findList'))
        l = po[0].findChildren("a",recursive=True)
        new_page = l[0]['href']
        driver.get(website + new_page)
        #NOW WE ARE ON THE CURRENT SHOWS PAGE. LEAVE THIS HERE IN CASE WE WANT THE SYNOPSIS OF THE WHOLE SHOW
        result = requests.get(driver.current_url)
        soup = BeautifulSoup(result.content)
        po = (soup.find_all('a', class_='bp_item np_episode_guide np_right_arrow'))
        for l in po:
            k = l
        #NOW WE ARE GOING TO GO TO THE EPISODE GUIDE AND GET TEH LAST EPISODE
        driver.get(website + new_page + "episodes")
        self.show_url = website+ new_page
        result = requests.get(website + new_page + "episodes")
        soup = BeautifulSoup(result.content)
        episode_scrape = soup.find_all('div', class_="ipl-rating-widget")
        most_recent_episode = episode_scrape[-1].parent
        links = most_recent_episode.findChildren("a", recursive=True)
        new_link = links[0]['href']
        driver.get(website+new_link)

        # we should gather both the summary and the plot synopsis IF IT SAYS 'PLOT SYNOPSIS' AND NOT 'ADD SYNOPSIS'
        #Plot storyline item
        result = requests.get(driver.current_url)
        soup = BeautifulSoup(result.content)
        synopsis = None
        item = (soup.find(id= 'titleStoryLine'))
        summary = item.findChildren("span", recursive=True)[1].text
        for anchor in item.findChildren("a", recursive=True):
            if anchor.text == "Plot Synopsis":
                driver.get(website + anchor['href'])
                result = requests.get(driver.current_url)
                soup = BeautifulSoup(result.content)
                item = soup.find(id="plot-synopsis-content")
                synopsis = item.text

        #this is the summary text
        if synopsis is not None:
            summary = synopsis
        self.summary = summary
        print(self.summary)

    def get_summary(self):
        return self.summary

    def prepare_corpus(self):

        content = None
        script_dir = os.path.dirname(__file__) 
        if path.exists(os.path.join(script_dir, "stemmed_words.txt")):
            print("file exists!")
            with open(os.path.join(script_dir, "stemmed_words.txt"), "r") as f:
                content = f.readlines()[0].split()
                #content is now an array of individual words
                print(len(content))
                print(content[5])
                self.content = content 
                return
        else:
            print("file doesn't exist!")
            with open(os.path.join(script_dir, "texts/news.2010.en.shuffled"), "r") as f:
                content = f.readlines()
            print("done reading")
            content = " ".join(content)
            print("done joining")
            content = (re.split(r'\W+', content))
            print("done regexing")
            content = " ".join([self.stemmer.stem(word) for word in content])
            print(len(content))
            self.content = content


scraper = WebScraper()
this_show = None
@app.route('/', methods=["GET"])
def test():
    return "Looks like it works!"


@app.route('/setup/corpus', methods=['GET'])
def display():
    scraper = WebScraper()
    scraper.prepare_corpus()
    words = scraper.get_content()
    with open("stemmed_words.txt", "w") as f:
        f.write(" ".join([word for word in words]))
    return "Corpus Created"

@app.route('/show=<show>', methods=['POST', 'GET'])
def addShow(show):
    print(show)
    scraper.scrape(show)
    words = scraper.model()
    return words

@app.route('/look', methods=['GET'])
def look():
    return scraper.get_list()

if __name__=='__main__':
    app.run(host="0.0.0.0", port="80")
