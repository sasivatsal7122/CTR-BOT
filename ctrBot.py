from urllib.parse import urlparse
import configparser

from googleBot import run_GoogleBot
from bingBot import run_BingBot
from youtubeBot import run_YoutubeBot


def read_settings():
    """Reads the settings from config.ini file and returns the values."""
    config = configparser.ConfigParser()
    config.read('config.ini')

    search_engine = config.get("CTR SETTINGS","SEARCH_ENGINE")
    target_url = config.get("CTR SETTINGS","TARGET_URL")
    keywords = config.get("CTR SETTINGS","KEYWORDS").split('\n')
    parsed_url = urlparse(target_url)
    target_domain_name = parsed_url.netloc
    
    return search_engine,target_url,keywords,target_domain_name

if __name__ == "__main__":

    search_engine,target_url,keywords,target_domain_name = read_settings()
    
    """Runs the bot for the selected search engine."""
    if search_engine == "Google" or search_engine == "google":
        
        print("Google selected.")
        run_GoogleBot(target_url,keywords,target_domain_name)
        
    elif search_engine == "Bing" or search_engine == "bing":
        
        print("Bing selected.")
        run_BingBot(target_url,keywords,target_domain_name)
        
    elif search_engine == "Youtube" or search_engine == "youtube":
        
        print("Youtube selected.")
        run_YoutubeBot(target_url,keywords)
    else:
        print("Search engine not supported yet.")
        