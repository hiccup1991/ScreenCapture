#!/usr/bin/env python

"""test_screencapture.py: captures a fullpage screenshot of a website."""

__author__ = "Thomas Abear"
__status__ = "Development"

import os
from datetime import datetime
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time

# selenium
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options = Options()
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--window-size=1920x1080')
browser = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)

# temp settings
url = "https://asana.com"
directory = 'screenshots'
time_limit = 20
time_interval = 2

# creates directory if it doesn't exist yet
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

def execute_screenshot(url, directory):
    create_project_dir(directory)
    filename = ("{}-{}".format(website_cleaner(url), datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))).replace("--","-")
    print("capturing screen: {}".format(filename))
    viewport = set_window_size() # captures the height
    browser.set_window_size(1920, viewport) # resets the window size to viewport dimensions
    set_window_size() # sets the page to full view
    browser.get_screenshot_as_file('./{}/{}.png'.format(directory,filename))
    browser.set_window_size(1920, 1080) # resets the window size to default

# sets the browser window size and captures the viewport height
def set_window_size():
    total_height = browser.execute_script("return document.body.parentNode.scrollHeight")
    viewport_height = browser.execute_script("return window.innerHeight")
    browser.set_window_size(1920, total_height)
    return viewport_height

# cleans the url and gets the first
def website_cleaner(web_url):
    web_url = "{}".format(web_url.replace("http://", ""))
    web_url = "{}".format(web_url.replace("https://", ""))
    web_url = "{}".format(web_url.replace("www.", ""))
    web_url = "{}".format(web_url.replace("web.archive.org/web/", "")) # cleaner for the wayback machine
    cleaned_web_url = "{}".format(web_url.replace("/", "-"))
    return cleaned_web_url

def main():
    time_start = time()

    browser.get(url)
    while (time()-time_start) < time_limit:
        execute_screenshot(url, directory)
        sleep(time_interval)
    browser.quit()

    time_end = time()
    time_elapsed = round((Decimal(time_end-time_start)),0)
    time_seconds = round((Decimal(time_elapsed%60)),0)
    time_minutes = int(time_elapsed/60)
    time_hours = int(time_minutes/60)
    print("\nScreenshot complete!\n\nTime duration: {} seconds\nHours: {}\nMinutes: {}\nSeconds: {}".format(str(time_elapsed), time_hours, (time_minutes-(time_hours*60)), time_seconds))

if __name__ == "__main__":
    main()
