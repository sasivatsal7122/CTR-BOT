from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import random
import time
from bs4 import BeautifulSoup
import time
from loguru import logger


logger.remove()
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
logger.add("logger.log", format=LOG_FORMAT)

def run_BingBot(target_url,keywords,target_domain_name):
    """Runs the bot for Bing search engine."""
    
    logger.info(f"STARTED BING BOT")
    
    print("Target URL:",target_url)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.maximize_window()
    print("Driver installed.")
    driver.get('https://www.bing.com/')
    driver.refresh()

    WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
    search_box = driver.find_element(By.NAME, "q")
    keyword = random.choice(keywords)
    print("Keyword:",keyword)

    for letter in keyword:
        search_box.send_keys(letter)
        time.sleep(random.randint(0,1000)/1000)

    time.sleep(2)

    search_box.send_keys(Keys.RETURN)

    time.sleep(5)

    flag = True;counter=1
   
    logger.info(f"\n\n\n ========= {keyword} ========= \n")
    logger.info(f"Searching for target domain: {target_url}")
    print("Searching for target domain:",target_domain_name)
    while flag:
        if counter>10:
            break
        logger.info(f"Currently in --> Page-{counter}")
        print(f"Currently in --> Page-{counter}")
        try:
            html_source = driver.page_source
            sourcedata = html_source.encode('utf-8')
            soup = BeautifulSoup( sourcedata , 'html.parser')
            
            search_results = soup.find_all("li", {"class": "b_algo"})
            for result in search_results:
                hyperlink = result.find("cite").text
                title = result.find("h2").text
                logger.info(f"{counter}.{hyperlink} \n")
            
                print(hyperlink,"-->",title)
                if target_domain_name in hyperlink:
                    target_title = title
                    print(f"====== Found The Link ======= at index - {counter}")
                    flag=False
                    break
            if flag:
                print("Going to next page...")
                next_button = driver.find_element(By.XPATH, "//a[@title='Next page']")
                
                desired_y = (next_button.size['height'] / 2) + next_button.location['y']
                window_h = driver.execute_script('return window.innerHeight')
                window_y = driver.execute_script('return window.pageYOffset')
                current_y = (window_h / 2) + window_y
                scroll_y_by = desired_y - current_y

                for i in range(1, int(scroll_y_by), 1):
                    driver.execute_script("window.scrollTo(0, {});".format(i))
                time.sleep(3)
                next_button.click()
                counter+=1
                time.sleep(5)
        except Exception as e:
            print(e)
            break
            

    if not flag:
        print("Target domain found in first 10 pages.")
        h2_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,target_title))
        )
        print("Scrolling to target domain.")
        try:
            desired_y = (h2_element.size['height'] / 2) + h2_element.location['y']
            window_h = driver.execute_script('return window.innerHeight')
            window_y = driver.execute_script('return window.pageYOffset')
            current_y = (window_h / 2) + window_y
            scroll_y_by = desired_y - current_y
        
            for i in range(1, int(scroll_y_by), 1):
                driver.execute_script("window.scrollTo(0, {});".format(i))
        except Exception as e:
            print(e)
            
        time.sleep(5)
        print("Clicking on target domain.")
        try:
            h2_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,target_title))
        )
            h2_element.click()
        except Exception as e:
             driver.get(target_url)
        print("Waiting for 10 seconds.")
        time.sleep(10)
        print("Target domain clicked.")
    else:
        print("Target domain not found in first 10 pages.")
        driver.get(target_url)
        print("Waiting for 10 seconds.")
        time.sleep(10)

    driver.quit()



