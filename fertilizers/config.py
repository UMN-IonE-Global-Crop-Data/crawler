import os
from selenium.webdriver import Chrome, ChromeOptions


tables = "CROPPING PATTERN"
downloads_path = os.getcwd()

chrome_options = ChromeOptions()
# ban CSS
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")

# set up default download path
prefs = {
    'download.default_directory': downloads_path,  
}
chrome_options.add_experimental_option("prefs", prefs)


table = "TABLE 4A-USAGE OF DIFFERENT FERTILIZERS FOR DIFFERENT CROPS"