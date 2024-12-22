import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

#libraries from bright data website
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

load_dotenv()
AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print("Launching Chrome Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        #captcha solver
        print("Waiting for captcha to solve..")
        solve_res = driver.execute('executeCdpCommand',{
            "cmd":"Captcha.waitForSolve",
            'params':{'detectTimeout':10000},
        })
        print('Captcha Solve Status:',solve_res['value']['status'])
        print("------"*10)
        # print('Taking page screenshot to file page.png')
        # driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
        return html

# -- Cleaning the html for proper presentation --    
#-- extracting the html body content --
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,"html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


#cleaning the body of the content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,"html.parser")
    for script_or_style in soup(["script","style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content


#creating batches of data as LLM have a limit of 8000 words hence we will create batches for easy processing
def split_dom_content(dom_content,max_length = 6000):
    return [
        dom_content[i:i + max_length] for i in range(0,len(dom_content),max_length)
    ]
    