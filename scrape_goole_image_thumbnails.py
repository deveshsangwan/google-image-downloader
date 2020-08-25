from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import time

urllib3.disable_warnings(InsecureRequestWarning)

searchword = input()
searchurl = ('https://www.google.com/search?q=' + searchword + '&source=lnms&tbm=isch')
dirs = 'pictures'
maxcount = 100
chrome_driver_path = "chromedriver.exe"
browser_path = "C:\\Users\\Devesh sangwan\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe" 

if not os.path.exists(dirs):
    os.mkdir(dirs)


def download_google_staticimages():

    options = webdriver.ChromeOptions()
    options.binary_location = browser_path
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    try:
        driver = webdriver.Chrome(executable_path = chrome_driver_path, chrome_options = options)
    except Exception as e:
        print('Chrome driver not found')
        print(f'exception: {e}')

    driver.set_window_size(1280, 1024)
    driver.get(searchurl)
    time.sleep(1)

    print('Downloading images')
    print('This may take a few moments...')

    element = driver.find_element_by_tag_name('body')

    # Scroll down
    # for i in range(30):
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        driver.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    print(f'Reached end of page.')
    time.sleep(0.5)
    print(f'Retry')
    time.sleep(0.5)

    # loading more results
    driver.find_element_by_xpath('//input[@value="Show more results"]').click()

    # Scroll down 2
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        driver.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    # elements = driver.find_elements_by_xpath('//div[@id="islrg"]')
    # page_source = elements[0].get_attribute('innerHTML')
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('img')

    urls = []
    for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print('Image sources not found')
                print(e)

    count = 0
    if urls:
        for url in urls:
            try:
                res = requests.get(url, verify=False, stream=True)
                rawdata = res.raw.read()
                with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                    f.write(rawdata)
                    count += 1
            except Exception as e:
                print('Failed to write')
                print(e)

    driver.close()
    return count


def main():
    t0 = time.time()
    count = download_google_staticimages()
    t1 = time.time()

    total_time = t1 - t0
    print(f'\n')
    print(f'Download completed. [Successful count = {count}].')
    print(f'Total time is {str(total_time)} seconds.')


if __name__ == '__main__':
    main()
