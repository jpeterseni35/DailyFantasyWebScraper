# A web scraper that pulls the probable pitchers and batters of the MLB games of the day. After receiving
# the probable players, it gathers daily projection data from public sources to find an aggregate value and
# stores them in a database. Finally, the program outputs the data, either displayed in the GUI or as a CSV
# file.


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
delay = 5  # seconds
driver.get('https://www.rotowire.com/daily/mlb/optimizer.php?site=DraftKings')

try:
    element = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located(
            (By.ID, "webix_ss_body"))
    )
# Time out garunteed so exception used to get elements
except:

    rotodk_header_element = driver.find_elements_by_class_name(
        "webix_ss_body")

    # rotodk_header_element = driver.find_element_by_css_selector("div[class^='webix_hcell']"))

    rotodk_header = []

    for item in rotodk_header_element:
        rotodk_header.append(item.text.strip())

finally:
    driver.quit()


print(f"{rotodk_header}")
