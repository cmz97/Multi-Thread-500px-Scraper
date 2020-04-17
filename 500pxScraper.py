from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import urllib.request as request
import uuid
from selenium.webdriver.firefox.options import Options
from PIL import ImageFile
import re
import time
import os.path
from os import path
import os

MIN_WIDTH = 300
MIN_HEIGHT = 300
MAX_RECAPTURE_TIME = 5
INFINITE_SCROLL_LOAD_WAIT_TIME = 2 #second
INFINITE_SCROLL_END_CONFIRM_REDUN = 2 # check lenght now change twice
IMAGE_PAGE_LOAD_TIMEOUT = 5
PORTFOLIO_PAGE_LOAD_TIMEOUT = 10
USER_NAME = "atomcollider"
STUCK_REFRESH_INTERVAL = 3

dir = os.path.join(os.getcwd(), USER_NAME)
nsfwDir = os.path.join(dir, "NSFW")
sfwDir = os.path.join(dir, "SFW")
PassedQualityCheck = False
infi_scroll_end_counter = 0
existingImgList = []
failedCaptureImageURLList = []


if not path.exists(dir):
    os.mkdir(dir)

if not path.exists(nsfwDir):
    os.mkdir(nsfwDir)

if not path.exists(sfwDir):
    os.mkdir(sfwDir)

for file in os.listdir(nsfwDir):
    if file.endswith(".jpg"): existingImgList.append(file)

for file in os.listdir(sfwDir):
    if file.endswith(".jpg"): existingImgList.append(file)

print("Found " + str(len(existingImgList)) + " Pre-existing Images")

def getsizes(uri):
    try:
        # get file size *and* image size (None if not known)
        file = request.urlopen(uri)
        size = file.headers.get("content-length")
        if size: size = int(size)
        p = ImageFile.Parser()
        while 1:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return p.image.size
                break
        file.close()
        return None
    except:
        return None


# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
driver.get('https://500px.com/' + USER_NAME)

imgPortfolio = WebDriverWait(driver, PORTFOLIO_PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div"))) # get element contain pictures from portfolio

last_height = driver.execute_script("return document.body.scrollHeight")

while infi_scroll_end_counter < INFINITE_SCROLL_END_CONFIRM_REDUN:
    print("Perform Scrolling Now")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(INFINITE_SCROLL_LOAD_WAIT_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        infi_scroll_end_counter += 1
    last_height = new_height

print("Page End Reached!")


portfolioElement = imgPortfolio.find_elements_by_tag_name('a')

imgUrlsFromProfile = {element.get_attribute('href') for element in portfolioElement if element.get_attribute('href') != None } # get image page url
print(imgUrlsFromProfile)

for index, url in enumerate(imgUrlsFromProfile):
    print("Processing URL: " + url)
    component = re.match(r"https?:\/\/(.+?)(\/.*)", url)
    metaInfo = component[2].split('/')[1:]
    recaptureCount = 0
    if len(metaInfo) == 3:
        id500px = metaInfo[1]
        title = metaInfo[2]
        ifsfw = True

        if str(title + "_" + id500px + ".jpg") not in existingImgList:
            driver.get(url)
            # wait for the select element to become visible

            while (not PassedQualityCheck):
                try:
                    select_element = WebDriverWait(driver, IMAGE_PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]"))) #SFW content
                except:
                    print("!!Timed Out Expection!!")
                    driver.refresh()
                    time.sleep(STUCK_REFRESH_INTERVAL)
                    break

                if select_element.find_elements_by_tag_name('img') == []:
                    ifsfw = False # NSFW Content
                    try:
                        select_element = WebDriverWait(driver, IMAGE_PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[3]"))) #NSFW content
                    except:
                        print("!!Timed Out Expection!!")
                        driver.refresh()
                        time.sleep(STUCK_REFRESH_INTERVAL)
                        break

                images = select_element.find_elements_by_tag_name('img')
                print("DEBUG! ----> " + str(images))

                for index, image in enumerate(images):
                    imgUrl = image.get_attribute('src')
                    print(">>>> Captured Img URL: " + imgUrl)
                    imgSize = getsizes(imgUrl)
                    imgSize = (0,0) if imgSize == None else imgSize # make sure the getsize function error get caught

                    if imgSize[0] > MIN_WIDTH and imgSize[1] > MIN_HEIGHT | recaptureCount > MAX_RECAPTURE_TIME:
                        print(">>>> Image Dimension: " + str(imgSize))
                        if recaptureCount > MAX_RECAPTURE_TIME:
                            print("Max Recapture Time Reached!!: ")
                            failedCaptureImageURLList.append(imgUrl)

                        if ifsfw:
                            request.urlretrieve(imgUrl, os.path.join(sfwDir, title + "_" + id500px + ".jpg"))
                        else:
                            request.urlretrieve(imgUrl, os.path.join(nsfwDir, title + "_" + id500px + ".jpg"))

                        PassedQualityCheck = True
                    else:
                        print(">>>> Quality Check Not Pass, Re-Capturing !!!!!")
                        recaptureCount += 1

            PassedQualityCheck = False
        else:
            print("Skiping " + title + "_" + id500px + ".jpg --- Already Exisit!")
    elif len(metaInfo) == 1:
        pass
    else:
        raise RuntimeError('[Error #1] Unexpected URL format, pls report This Bug on github!')


driver.quit()
print("Job Complete, Created by Chengming Kevin Zhang 2020")
