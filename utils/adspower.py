import http.client
import json
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service

def start_profile(profile_id):
    conn = http.client.HTTPConnection("localhost:50325")
    payload = ""
    headers = { 'User-Agent': "insomnia/10.0.0" }
    conn.request("GET", f"/api/v1/browser/start?user_id={profile_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded = data.decode("utf-8")
    res_json = json.loads(decoded)
    return res_json

def stop_profile(profile_id):
    conn = http.client.HTTPConnection("localhost:50325")
    payload = ""
    headers = { 'User-Agent': "insomnia/10.0.0" }
    conn.request("GET", f"/api/v1/browser/stop?user_id={profile_id}", payload, headers)

def get_driver(profile_response: str, options: webdriver.ChromeOptions) -> webdriver.Chrome:
    address = profile_response['data']['ws']['selenium']
    webdriver_src = profile_response['data']['webdriver']
    chrome_drive_path = Service(webdriver_src)
    options.debugger_address = address

    driver = webdriver.Chrome(service=chrome_drive_path, options=options)
    return driver