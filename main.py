import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Open tab in incognito mode in order to avoid previous data being loaded, such as
# cookies, site data or information entered in forms saved on the device.
# Setting experimental option 'detach' to True in order to window stay open
options = Options()
options.add_argument("--incognito")
options.add_experimental_option('detach', True)

# Get the webdriver path for Linkedin Homepage.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
url = 'https://www.linkedin.com/home'
driver.get(url)

time.sleep(2)

# Find the input field for signing in on Linkedin home page.
email = driver.find_element(By.XPATH, "//input[@name = 'session_key']")
password = driver.find_element(By.XPATH, "//input[@name = 'session_password']")

# Read email and password from different text files saved on device and insert.
with open(r"C:\Users\Loki\Desktop\in.keys\email.txt") as User:
    username = User.read().replace('\n', '')
email.send_keys(username)

with open(r"C:\Users\Loki\Desktop\in.keys\password.txt") as Pass:
    passcode = Pass.read().replace('\n', '')
password.send_keys(passcode)

time.sleep(2)

submit = driver.find_element(By.XPATH, "//button[@type = 'submit']").click()
time.sleep(3)










