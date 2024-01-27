from time import sleep
import selenium_dolphin as dolphin
import logging
from settings import DRIVER_PATH
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Client:
    def __init__(self, profile_id: str) -> None:
        # WORK ONLY FOR RUSSIAN LANGUAGE ACCOUNTS.

        response = dolphin.run_profile(profile_id)
        port = response['automation']['port']
        options = Options()
        options.add_argument("--start-maximized")

        self.driver = dolphin.get_driver(
            options=options,
            port=port,
            driver_path=DRIVER_PATH
        )
        self.profile_id = profile_id

    def share_to_groups(self, post_link: str):
        self.driver.get(post_link)
        logging.info(f"[{self.profile_id}] {self.driver.title}")
        sleep(1)

        last_groups = []

        while True:
            try:
                self.driver.find_element(
                    By.CSS_SELECTOR, "[data-widget-item-type=\"reshare\"]"
                ).click()
            except:
                # When group'll be succesful completed program move to POST PAGE where'll be share button, BUT if all groups'll be added then in FOR willn't called "break" and in new cycle "reshare" button'll not be found
                logging.info(f"[{self.profile_id}] All groups added")
                break

            sleep(2)

            self.driver.find_element(
                By.LINK_TEXT, "Поделиться в группе" 
            ).click()

            sleep(2)

            groups = self.driver.find_elements(
                By.CSS_SELECTOR, "[id^=\"reshare_XpostGroupSuggest_\"]>div>:nth-child(2)>:first-child"
            )
            
            if len(groups) == 0:
                logging.info(f"[{self.profile_id}] Can't locate available groups in account {groups}")
                break

            for group in groups:
                group_name = group.text
                if group_name not in last_groups:
                    logging.info(f"[{self.profile_id}] Sending post to {group_name}")
                    group.click()

                    sleep(2)
                    self.driver.find_element(
                        By.CSS_SELECTOR, "[data-l=\"t,button.submit\"]"
                    ).click()
                    last_groups.append(group_name)
                    break

            logging.info(f"[{self.profile_id}] Reposting to another group")
            sleep(5)

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