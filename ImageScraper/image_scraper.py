import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import *
import time

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url, driver):
    """
    Returns all image URLs on a single `url`
    """
    extensions = {"jpg", "jpeg", "png", "gif"}
    html = driver.page_source.split('"')
    urls = []
    for i in html:
        if (i.startswith('http') or i.startswith('//')) and 'jpg' in i.split('.')[-1]:     #starting with http or // and ending with jpg (as a part)
            if(i.startswith('http')):
                urls.append(i.split('"')[0])
            else:
                urls.append('http:'+i.split('"')[0])
    print(urls)
    img_type = []   
    print ("Total images: {}\n".format(len(urls)))
    return urls


def download(url, pathname, count):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, str(count) +".jpg")

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    count += 1
    return count

def img_download(url, path, count):
    # get all images
    chrome_driver_path = "D:\\programming\\Machine learning\\ml_projects\\google image scraper\\chromedriver.exe"  
    browser_path = "C:\\Users\\Devesh sangwan\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe" 
    option = webdriver.ChromeOptions()
    option.binary_location = browser_path 
    driver = webdriver.Chrome(executable_path = chrome_driver_path, chrome_options = option)
    driver.get(url)
    #time.sleep(10)
    for __ in range(10):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(.2)
    imgs = get_all_images(url, driver)
    for img in imgs:
        # for each img, download it
        count = download(img, path, count)
    return count
    #driver.quit()

