import http.client
import json
from time import sleep
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service

from utils.adspower import get_driver, start_profile, stop_profile 

res_json = start_profile("kn1nma0")

driver = get_driver(res_json)

sleep(2)

driver.get("https://ok.ru")

sleep(5)
stop_profile("kn1nma0")