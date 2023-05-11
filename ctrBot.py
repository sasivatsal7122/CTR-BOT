from urllib.parse import urlparse
import configparser
import random

from googleBot import run_GoogleBot
from bingBot import run_BingBot
from youtubeBot import run_YoutubeBot

# ==== CHHOSE THE CONFIGURATION HERE ====
# YOU CAN CHHOSE BETWEEN 3 CONFIGURATIONS: 1,2,3
CONFIG=1

def read_settings():
    """Reads the settings from config.ini file and returns the values."""
    
    print(f"running config {CONFIG}")
    config = configparser.ConfigParser()
    config.read(f'config{CONFIG}.ini')

    search_engine = config.get("CTR SETTINGS","SEARCH_ENGINE")
    target_url = config.get("CTR SETTINGS","TARGET_URL").split('\n')
    alternate_target_urL = config.get("CTR SETTINGS","ALTERNATE_TARGET_URL")
    keywords = config.get("CTR SETTINGS","KEYWORDS").split('\n')
    
    if CONFIG==1 or CONFIG==2:
        target_url = random.choice(target_url)
        keyword = random.choice(keywords)
    elif CONFIG==3:
        targetUrl_keyword_dict = dict(zip(target_url,keywords))
        target_url = random.choice(list(targetUrl_keyword_dict.keys()))
        keyword = targetUrl_keyword_dict[target_url]
    
    return search_engine,target_url,alternate_target_urL,keyword

if __name__ == "__main__":

    search_engine,target_url,alternate_target_urL,keyword = read_settings()
    
    """Runs the bot for the selected search engine."""
    if search_engine == "Google" or search_engine == "google":
        
        print("Google selected.")
        run_GoogleBot(target_url,keyword,alternate_target_urL)
        
    elif search_engine == "Bing" or search_engine == "bing":
        
        print("Bing selected.")
        run_BingBot(target_url,keyword,alternate_target_urL)
        
    elif search_engine == "Youtube" or search_engine == "youtube":
        
        print("Youtube selected.")
        run_YoutubeBot(target_url,keyword,alternate_target_urL)
    else:
        print("Search engine not supported yet.")
        