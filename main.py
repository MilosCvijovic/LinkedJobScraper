from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import re


# Open tab in incognito mode in order to avoid previous data being loaded, such as
# cookies, site data or information entered in forms saved on the device.
options = Options()
options.add_argument("--incognito")
# Setting experimental option 'detach' to True in order to window stay open.
options.add_experimental_option('detach', True)

# Get the web driver path for Linkedin Homepage.
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

# Click login in button.
driver.find_element(By.XPATH, "//button[@type = 'submit']").click()
time.sleep(2)

# Go to the 'Jobs' page with already added parameters.
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3247607301&geoId=101855366&keywords=python%20internship&location=Serbia&refresh=true")
time.sleep(3)

# Try to load pages if there are moore then one
try:
    for i in range(1, 3):
        # click button to change the job list
        driver.find_element(By.XPATH, f'//button[@aria-label="Page {i}"]').click()
        time.sleep(2)
except:
    pass

# Scroll down all job offers to collect necessary information.
element = driver.find_element(By.XPATH, '//*[@id="main"]/div/section[1]/div')
for i in range(20):
    driver.execute_script("arguments[0].scrollBy(0, 500)", element)
    time.sleep(2)

# Collecting data to extract(job titles, location, company name).
job_src = driver.page_source
soup = BeautifulSoup(job_src, 'lxml')

jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})

job_titles = []

for title in jobs_html:
    job_titles.append(title.text.strip())

print(job_titles)

location_html = soup.find_all(
    'ul', {'class': 'job-card-container__metadata-wrapper'})

location_list = []

for loc in location_html:
    res = re.sub('\n\n +', ' ', loc.text.strip())

    location_list.append(res)

print(location_list)


company_name_html = soup.find_all(
    'a', {'class': 'job-card-container__company-name'})
company_names = []

for name in company_name_html:
    company_names.append(name.text.strip())

print(company_names)


# Creating a Dataframe with list
df = pd.DataFrame(list(zip(job_titles, location_list, company_names)))

# exporting our dataframe to a csv file
df.to_csv('jobs.csv', sep=';')
