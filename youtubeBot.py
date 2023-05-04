from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from proxy import get_proxy


import random
import time
from loguru import logger
import yt_dlp
from fake_useragent import UserAgent


logger.remove()
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
logger.add("logger.log", format=LOG_FORMAT)

def run_YoutubeBot(target_vid_link,keywords):   
    
    """ Runs the bot for Youtube search engine."""

    logger.info(f"STARTED YOUTUBE BOT")
    
    print("Target video link:",target_vid_link)
    logger.info(f"Target video link: {target_vid_link}")
    
    user_agent = user_agent = UserAgent().random
    print("User agent:",user_agent)
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    seleniumwire_options = get_proxy()
    driver = webdriver.Firefox(seleniumwire_options=seleniumwire_options,service=Service(GeckoDriverManager().install()))
    print("Driver installed.")
    driver.maximize_window()

    driver.get("https://www.google.com/")
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
    keyword = "youtube"

    for letter in keyword:
        search_box.send_keys(letter)
        time.sleep(random.randint(0,1000)/1000)

    time.sleep(2)

    search_box.send_keys(Keys.RETURN)

    time.sleep(5)
    print("Searching for youtube.com link...")
    div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//div[a/@href="https://www.youtube.com/"]'))
        )
    h3_element = div_element.find_element(By.XPATH, './/h3')
    h3_element.click()

    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "search_query")))
    search_box.click()
    print("Searching for video...")
    yt_keyword = random.choice(keywords)
    print("Keyword:",yt_keyword)
    
    logger.info(f"Keyword: {yt_keyword}")
    for letter in yt_keyword:
        search_box.send_keys(letter)
        time.sleep(random.randint(0,1000)/1000)

    time.sleep(2)
    search_box.send_keys(Keys.ENTER)

    WebDriverWait(driver, 60).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a#video-title")
    ))
    
    driver.refresh()
    time.sleep(10)

    WebDriverWait(driver, 60).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a#video-title")
    ))
    
    print("Scrolling down...")

    last_index = 0 
    target_not_found = True
    while target_not_found:
        if last_index>100:
            break
            
        video_links = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
        video_links = video_links[last_index:]
        for video in video_links:
            print(video.get_attribute("href"))
            logger.info(f"Video link: {video.get_attribute('href')}")
            if target_vid_link in video.get_attribute("href"):
                print("==== Video FOUND =====")
                target_not_found = False
                break
            else:
                driver.execute_script("arguments[0].scrollIntoView({block: 'start', inline: 'nearest', behavior: 'smooth'});", video)
                time.sleep(0.5)
            last_index += 1
        time.sleep(5)
        
    if not target_not_found:
        print("Clicking on video link...")
        time.sleep(3)
        video.click()
        print("Video clicked.")
        print("Waiting for video to load...")
        
        with yt_dlp.YoutubeDL({}) as ydl:
            video_info = ydl.extract_info(target_vid_link, download=False)
            video_length = video_info.get('duration')
            
        print("Total duration:",video_length)
        watch_percentage = random.uniform(0.8, 0.99)
        print("Choosen Watch percentage:",watch_percentage)
        watch_duration = int(video_length * watch_percentage)
        print("Watching video for :",watch_duration,"secs")
        time.sleep(watch_duration)
    else:
        print("Video not found.")
        print("Opening the target directly")
        driver.get(target_vid_link)
        print("Waiting for video to load...")
        
        with yt_dlp.YoutubeDL({}) as ydl:
            video_info = ydl.extract_info(target_vid_link, download=False)
            video_length = video_info.get('duration')
            
        print("Total duration:",video_length)
        watch_percentage = random.uniform(0.8, 0.99)
        print("Choosen Watch percentage:",round(watch_percentage,2))
        watch_duration = int(video_length * watch_percentage)
        print("Watching video for :",round(watch_duration,2),"secs")
        time.sleep(watch_duration)
        
    driver.quit()

