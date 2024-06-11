from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

app = Flask(__name__)

def scrape_poems():
    ROOT = "https://smart.poems.com.sg/smartpark/"
    website = ROOT
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(website)

    box = driver.find_element(By.CSS_SELECTOR, "div[class='cpark']").find_element(By.CSS_SELECTOR, "div[class='boxedcontent']")
    section = box.find_element(By.CSS_SELECTOR, "section[class='introblock whites brow-section calltoactionarea page_relative ware-of-invest']")
    return_div = section.find_element(By.CSS_SELECTOR, "div[class='mob']")
    sgd = return_div.find_element(By.XPATH, ".//p[5]").text
    usd = return_div.find_element(By.XPATH, ".//p[6]").text
    return {
        "sgd": sgd,
        "usd": usd
    }


@app.route("/", methods=['GET'])
async def get_data():
    result = scrape_poems()
    return json.dumps(result)

if __name__ == '__main__':
    app.run(port=7777)