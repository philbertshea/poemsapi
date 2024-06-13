from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def scrape_poems():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    ROOT = "https://smart.poems.com.sg/smartpark/"
    website = ROOT
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


@app.route("/", methods=['GET', 'POST'])
def get_data():
    if (request.method == 'GET'):
        result = scrape_poems()
        return result

if __name__ == '__main__':
    app.run(port=7777)