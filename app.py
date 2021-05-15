import os
import time
import urllib.parse

from flask import Flask
from flask import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import constants


app= Flask(__name__)

driver = None
wait = None
CHROMEDRIVER_PATH = os.path.join(app.root_path, "bin/chromedriver")

def get_lyrics_url(artist, track):
    search_query = urllib.parse.quote(artist.strip() + " " + track.strip() + " " + "lyrics")
    search_url = constants.LYRICS_PROVIDER + "?q=" + search_query

    return search_url


def get_lyrics_from_url(url):
    driver.get(url)
    time.sleep(3)
    
    print("class name = " + constants.LYRICS_EXPAND_CLASS_NAME)
    #print("page source = \n" + driver.page_source)

    #print(len(driver.find_elements_by_xpath("//div[@class='{}']".format(constants.LYRICS_EXPAND_CLASS_NAME))))

    driver.find_elements_by_xpath("//div[@class='{}']".format(constants.LYRICS_EXPAND_CLASS_NAME))[0].send_keys(Keys.ENTER)

    time.sleep(2)
    lyrics_div = driver.find_elements_by_xpath("//div[@class='{}']".format(constants.LYRICS_DIV_CLASS_NAME))[0]

    return lyrics_div.text.strip()


## improve this, can't keep instantiating driver for every request, can't keep the same either
## find a way to work on tab level
def setup_selenium():
    global driver, CHROMEDRIVER_PATH, wait
    
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
    wait = WebDriverWait(driver, 600)


@app.route('/')
def index():
    artist = request.args.get('artist', default = None, type = str)
    track = request.args.get('track', default = None, type = str)

    if artist is None or track is None:
        return "invalid artist/track", 400

    setup_selenium()

    lyrics_url = get_lyrics_url(artist, track)
    lyrics = get_lyrics_from_url(lyrics_url)

    driver.quit()

    if lyrics is None:
        return "error retrieving lyrics", 404

    return lyrics

if __name__ == '__main__':
    app.run()