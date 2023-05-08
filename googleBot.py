from selenium.webdriver.firefox.service import Service

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException
from seleniumwire import webdriver

import random
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import time
from loguru import logger
from fake_useragent import UserAgent
from proxy import get_proxy

logger.remove()
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
logger.add("logger.log", format=LOG_FORMAT)

def run_GoogleBot(target_url,keywords,alternate_target_urL):
    
    """Runs the bot for Google search engine."""
    found_urls = []
    url_titles = []
    
    logger.info(f"STARTED GOOGLE BOT")

    user_agent = UserAgent().random
    print("User agent:",user_agent)
    
    seleniumwire_options = get_proxy()
    #driver = webdriver.Firefox(seleniumwire_options=seleniumwire_options,service=Service(GeckoDriverManager().install()))
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.maximize_window()
    print("Driver installed.")
    driver.get("https://www.google.com/")
    driver.refresh()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "L2AGLb"))
        )
        element.click()
        time.sleep(5)
    except:
        print("No cookies popup found.")

    WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
    search_box = driver.find_element(By.NAME, "q")
    keyword = random.choice(keywords)
    target_url = random.choice(target_url)
    print("Target URL:",target_url)
    print("Keyword:",keyword)
    for letter in keyword:
        search_box.send_keys(letter)
        time.sleep(random.randint(0,1000)/1000)
    time.sleep(2)

    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g')))
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g')))
    flag = True;counter=1
    
    logger.info(f"\n\n\n ========= {keyword} ========= \n")
    logger.info(f"Searching for target domain: {target_url}")
    print("Searching for target domain:",target_url)
    while flag:
        if counter>10:
            break
        logger.info(f"Currently in --> Page-{counter}")
        print(f"Currently in --> Page-{counter}")
        try:
            
            html_source = driver.page_source
            sourcedata = html_source.encode('utf-8')
            soup = BeautifulSoup( sourcedata , 'html.parser')
            
            search_results = soup.select(".g")
            for result in search_results:
                hyperlink = result.find("a")["href"]
                title = result.find("h3").text
                
                found_urls.append(hyperlink)
                url_titles.append(title)
                logger.info(f"{counter}.{hyperlink} \n")
                
                print(hyperlink,"-->",title)
                if target_url in hyperlink:
                    target_title = title
                    print(f"====== Found The Link ======= at index - {counter}")
                    flag=False
                    break
            if flag:
                print("Going to next page...")
                next_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//a[@id='pnnext']"))
                        )
                
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
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", h2_element)
            h2_element.click()
        except (TimeoutException,ElementNotInteractableException):
             driver.get(target_url)
        print("Target domain clicked.")
        sleep_time = random.uniform(60, 60*2) 
        print(f"Waiting for {round(sleep_time,2)} seconds.")
        time.sleep(sleep_time)
    else:
        print("Target domain not found in first 10 pages.")
        driver.get(alternate_target_urL)
        sleep_time = random.uniform(60, 60*2) 
        print(f"Waiting for {round(sleep_time,2)} seconds.")
        time.sleep(sleep_time)
    
    now = datetime.utcnow()
    utc_timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    # Create a new DataFrame for the current run
    new_data = pd.DataFrame({
        "search engine": ["Google"] * len(found_urls),
        "Keyword": [keyword] * len(found_urls),
        "Found URLs": found_urls,
        "URL Title": url_titles,
        "UTC": [utc_timestamp] * len(found_urls)
    })
    
    try:
        existing_df = pd.read_excel("logs.xlsx")
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    # Concatenate the existing and new data
    combined_df = pd.concat([existing_df, new_data], ignore_index=True)

    # Save the combined DataFrame to the Excel file
    combined_df.to_excel("logs.xlsx", index=False)
        
    driver.quit()




