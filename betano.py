from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import json
import consts
import time
 
service = Service(executable_path="chromedriver.exe")
browser = uc.Chrome(service=service)

browser.get("https://www.betano.cz/sport/fotbal/nadchazejici-zapasy-dnes/")

time.sleep(5)

try:
    browser.find_element(By.XPATH, '//*[@id="landing-page-modal"]/div/div[1]/button').click()
except: pass

time.sleep(5)


wrapper = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section[2]/div[4]/div[2]/section/div[2]/div/div/div/div[2]/div/div[2]')
matches = wrapper.find_elements(By.XPATH, "//div[@data-evtid]")

matchData = []

for i, match in enumerate(matches):

    # Extract match date
    dates = match.find_elements(By.XPATH, './div[1]/div[1]/span')

    if(len(dates) != 2): continue

    date = dates[0].text.replace(" ", " ").strip()
    dateTime = dates[1].text.replace(" ", " ").strip()

    # Extract match title
    title = match.find_element(By.XPATH, './/div[@data-qa="participants"]')

    firstTeam = title.find_element(By.XPATH, './div[1]/div').get_attribute("textContent").replace(" ", " ").strip()
    secondTeam = title.find_element(By.XPATH, './div[2]/div').get_attribute("textContent").replace(" ", " ").strip()

    # Extract odds
    oddsElements = match.find_elements(By.XPATH, ".//div[contains(@role, 'button')]")
    odds = {}

    for oddElIndx, oddsElement in enumerate(oddsElements):
        odd = oddsElement.find_elements(By.XPATH, ".//span")

        if(len(odd) == 1):
            if(oddElIndx == 0):
                odds["1"] = odd[0].text
            if(oddElIndx == 1):
                odds["0"] = odd[0].text
            if(oddElIndx == 2):
                odds["2"] = odd[0].text

        if(len(odd) == 2):
            odds[odd[0].text] = odd[1].text

        
    # Append match data to the list
    matchData.append({
        "title": "{} - {}".format(firstTeam, secondTeam),
        "date":  "{}, {}".format(date, dateTime),
        "odds": odds
    })

# Create a dictionary with match data
data = {"matches": matchData}

# Write data to a JSON file
with open("betano-matches.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)

browser.quit()
