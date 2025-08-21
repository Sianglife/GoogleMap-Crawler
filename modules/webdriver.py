from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--lang=zh-TW')
options.add_argument("--force-device-scale-factor=0.75")  # scale to 75% for larger element visibility
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)
