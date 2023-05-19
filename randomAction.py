import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

def smooth_scroll_to_top(driver):
    current_scroll_position = driver.execute_script("return window.pageYOffset;")
    step = -50  # Scroll step (pixels)
    delay = 0.02  # Delay between steps (seconds)

    while current_scroll_position > 0:
        next_scroll_position = max(current_scroll_position + step, 0)
        driver.execute_script(f"window.scrollTo(0, {next_scroll_position});")
        current_scroll_position = next_scroll_position
        time.sleep(delay)
        
def human_click(driver, num_clicks=1):
    TRIES = num_clicks * 3
    
    while num_clicks:
        
        if not TRIES:
            break
        
        try:
            clickable_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//button | //a'))
            )

            print("Click iteration:", num_clicks)

            if clickable_elements:
                random_element = random.choice(clickable_elements)

                desired_y = (random_element.size['height'] / 2) + random_element.location['y']
                window_h = driver.execute_script('return window.innerHeight')
                window_y = driver.execute_script('return window.pageYOffset')
                current_y = (window_h / 2) + window_y
                scroll_y_by = desired_y - current_y

                for i in range(1, int(scroll_y_by), 1):
                    driver.execute_script("window.scrollTo(0, {});".format(i))

                if random_element.is_displayed():
                    actions = ActionChains(driver)
                    actions.key_down(Keys.CONTROL).click(random_element).key_up(Keys.CONTROL).perform()

                    # Get the current window handles
                    window_handles = driver.window_handles

                    if len(window_handles) > 1:
                        # Switch to the newly opened tab
                        driver.switch_to.window(window_handles[-1])
                        print("Switched to new tab")
                        time.sleep(10)

                        driver.close()
                        # Switch back to the original window
                        driver.switch_to.window(window_handles[0])
                        print("Closed new tab and switched back to the original tab")
                        time.sleep(10)
                        num_clicks -= 1

                    else:
                        print("New window not opened. Skipping tab switch.")
                        time.sleep(5)

            # Scroll to the top of the page smoothly
            smooth_scroll_to_top(driver)
            print("Scrolled to the top of the page")
            time.sleep(5)
            TRIES -= 1

        except Exception as e:
            print("An error occurred:", str(e))
            break