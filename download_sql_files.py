"""
This python script will download all the .sql files from my
(corey-hermesch) database-exercises github repo
"""

### IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time as t
import os

### SET VARIABLES
# get local env variables 
user = os.getenv('githubUSER')
pswd = os.getenv('githubPSWD')
# set base/page urls for working with github
base_url = 'https://github.com/'
page_url = '/database-exercises/'

### FUNCTIONS
def github_login(driver):
    """
    This function will
    - accept a Chrome webdriver (selenium object)
    - log in to github 
    - return
    """
    # set window size (by pixels)
    driver.set_window_size(1400, 1000)
    # navigate to github and log in
    driver.get(base_url+"login")
    # enter username and password and click login
    driver.find_element(By.NAME, 'login').send_keys(user)
    driver.find_element(By.NAME, 'password').send_keys(pswd)
    driver.find_element(By.NAME, 'commit').click()
    # this code ensures all of the file links load before we moveon
    t.sleep(3)

    return

def get_sql_files(driver):
    """
    This function will 
    - accept a Chrome webdriver (selenium object)
    - navigate to page_url ('database-exercises')
    - download all .sql files
    """
    # navigate to database-exercises
    driver.get(base_url+user+page_url)

    # get a list of filename 'elements' from the webpage using XPATH
    element_list = driver.find_elements(By.XPATH, '//a[@class="js-navigation-open Link--primary"]')
    # from 0 - length of element_list (num of file link 'object's) iterate...
    for i in range(0, len(element_list)):
        # had to use WebDriverWait everytime we start at a new page and 
        # had to re-ask for the filename elements & assign them to a variable
        new_element_list = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="js-navigation-open Link--primary"]')))
        # if the filename ends in .sql we want to download it
        if new_element_list[i].text[-4:] == '.sql':
            print(f'Downloading {new_element_list[i].text}')
            # click through to get to the page with the download button
            new_element_list[i].click()
            # assign the download button element to a variable (need a wait in here to account for page loading time
            dlbutton = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-component="IconButton"][@aria-label="Download raw content"]')))
            # move 'mouse' to the download button (not sure if this is required)
            ActionChains(driver).move_to_element(dlbutton).perform()
            # click the dlbutton to download
            dlbutton.click()
            # go back a page and start over
            driver.back()
    
    
### SCRIPT

# create webdriver object (which opens a chrome web browser window)
driver = webdriver.Chrome(service=Service())

# go to github and login
github_login(driver)

# download all .sql files from page_url
get_sql_files(driver)

# quit the driver
driver.quit()