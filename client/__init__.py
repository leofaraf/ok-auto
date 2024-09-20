from lib2to3.pgen2 import driver
from time import sleep
import selenium_dolphin as dolphin
import logging
from settings import DRIVER_PATH
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException


class Client:
    def __init__(self, profile_id: str) -> None:
        # WORK ONLY FOR RUSSIAN LANGUAGE ACCOUNTS.

        self.profile_id = profile_id
        response = dolphin.run_profile(profile_id)
        print("Response: {}.".format(response))
        port = response['automation']['port']
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        self.driver = dolphin.get_driver(
            options=options,
            port=port,
            driver_path=DRIVER_PATH
        )

    def click(self, element):
        wait = WebDriverWait(self.driver, 20)
        try:
            el = wait.until(EC.element_to_be_clickable(element))
            el.click()

        except ElementClickInterceptedException:
            logging.error("Trying to click on the button again")
            self.driver.execute_script("arguments[0].click()", el)


    def find_groups(self):
        def find_elements():
            return self.driver.find_elements(
                    By.CSS_SELECTOR, "[id^=\"reshare_XpostGroupSuggest_\"]>div>:nth-child(2)>:first-child"
            )
        
        while True:
            groups = find_elements()

            self.move_mouse_to(
                groups[-1]
            )
            sleep(.3)

            new_groups = find_elements()
        
            if len(groups) == len(new_groups):
                return new_groups


    def share_to_groups(self, post_link: str):

        self.driver.get(post_link)
        logging.info(f"[{self.profile_id}] {self.driver.title}")
        sleep(1)

        last_groups = []

        while True:
            try:
                self.click(
                    self.driver.find_element(
                        By.CSS_SELECTOR, "[data-widget-item-type=\"reshare\"]>div>.__inactive>button"
                    )
                )
            except Exception as e:
                # When group'll be succesful completed program move to POST PAGE where'll be share button, BUT if all groups'll be added then in FOR willn't called "break" and in new cycle "reshare" button'll not be found
                logging.info(f"[{self.profile_id}] All groups added ({e})")
                break

            sleep(2)

            self.driver.find_element(
                By.LINK_TEXT, "Поделиться в группе" 
            ).click()

            sleep(2)

            for group in self.find_groups():
                group_name = group.text
                self.move_mouse_to(
                    group
                )
                sleep(0.2)
                if group_name not in last_groups:
                    logging.info(f"[{self.profile_id}] Sending post to {group_name}")
                    
                    group.click()

                    sleep(1)
                    self.driver.find_element(
                        By.CSS_SELECTOR, "[data-l=\"t,button.submit\"]"
                    ).click()
                    last_groups.append(group_name)
                    break

            logging.info(f"[{self.profile_id}] Reposting to another group")
            sleep(5)

    def move_mouse_to(self, element):
        ActionChains(self.driver)\
            .move_to_element(element)\
            .perform()

    def __del__(self) -> None:
        """
        To remove object and client from online use "del".

        Input: 
        - client = Client(id)
        - del client

        Output:
        - [1238103218] Exiting...
        """
        logging.info(f"[{self.profile_id}] Exiting...")
        self.driver.quit()
        dolphin.close_profile(self.profile_id)
