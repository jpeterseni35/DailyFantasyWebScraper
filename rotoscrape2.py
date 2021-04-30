# A web scraper that pulls the probable pitchers and batters of the MLB games of the day. After receiving
# the probable players, it gathers daily projection data from public sources to find an aggregate value and
# stores them in a database. Finally, the program outputs the data, either displayed in the GUI or as a CSV
# file.


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.get('https://www.rotowire.com/daily/mlb/optimizer.php?site=DraftKings')
delay = 3  # seconds
try:
    myElem = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.ID, 'webix_ss_header')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

rotodk_data = driver.find_elements_by_class_name("webix_ss_header")
rotodk_header = []
for item in rotodk_data:

    rotodk_header.append(item.text.strip())


driver.close()

print(rotodk_header)

# rotodk_soup = BeautifulSoup(rotodk_html, 'html.parser')


# for line in rotodk_soup.findAll('div', attrs={'column': '1'}):
#     rotodk_data.append(line.text)


# print(rotodk_data)
