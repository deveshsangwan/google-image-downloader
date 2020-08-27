from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
from urllib.request import *
import sys
import time
import ImageScraper.image_scraper as img_scp

# adding path to chromedriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset1/"


def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def main():
    searchtext = input()
    num_requested = int(input())
    number_of_scrolls = num_requested / 400 + 1
    # number_of_scrolls * 400 images will be opened in the browser

    if not os.path.exists(download_path + searchtext.replace(" ", "_")):
        os.makedirs(download_path + searchtext.replace(" ", "_"))

    url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
    chrome_driver_path = "chromedriver.exe"
    browser_path = "C:\\Users\\Devesh sangwan\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    option = webdriver.ChromeOptions()
    option.binary_location = browser_path
    driver = webdriver.Chrome(
        executable_path=chrome_driver_path, chrome_options=option)
    driver.get(url)

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    extensions = {"jpg", "jpeg", "png", "gif"}
    img_count = 0
    downloaded_img_count = 0

    for _ in range(int(number_of_scrolls)):
        for __ in range(15):
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(0.2)
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath(
                "//input[@value='Show more results']").click()
        except Exception as e:
            print("Less images found: {}".format(e))
            break

    html = driver.page_source.split('"')
    imges = []
    links = []
    for i in html:
        if i.startswith('https:') and ('gstatic' not in i) and ('google' not in i):
            links.append(i.split('"')[0])
    for i in html:
        if i.startswith('http') and 'usqp=CAU' in i.split('.')[-1]:
            imges.append(i.split('"')[0])
    for i in html:
        if i.startswith('http') and i.split('"')[0].split('.')[-1] in extensions:
            imges.append(i.split('"')[0])
    links = list(set(links))
    imges = list(set(imges))
    print(imges)
    links_left = Diff(links, imges)
    file1 = open("page_source.txt", "w", encoding='utf8')
    file1.writelines(links_left)
    img_type = []
    print("Total images: {}\n".format(len(imges)))
    for img in imges:
        img_count += 1
        print("Downloading image {}:{}".format(img_count, img))
        img_type = img.rsplit('.', 1)
        try:
            req = Request(img, headers=headers)
            raw_img = urlopen(req).read()
            f = open(download_path+searchtext.replace(" ", "_")+"/" +
                     str(downloaded_img_count)+"."+"jpeg", "wb")
            f.write(raw_img)
            f.close
            downloaded_img_count += 1
        except Exception as e:
            print("Download failed: {}".format(e))
        finally:
            print
        if downloaded_img_count >= num_requested:
            break

    print("Total downloaded: {}/{}".format(downloaded_img_count, img_count))
    print("Total images: {}\n".format(len(links_left)))

    for url in links_left:
        img_count = img_scp.img_download(url, download_path+searchtext.replace(" ", "_")+"/", img_count)
    driver.quit()


if __name__ == "__main__":
    main()
