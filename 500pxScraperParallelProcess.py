from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import urllib.request as request
from selenium.webdriver.firefox.options import Options
from PIL import ImageFile
import re
import time
import os.path
from os import path
import os
from tqdm import tqdm
from enum import Enum
import threading
import argparse


def init_Parser():
    argparse.ArgumentParser(description='Selenium based mutilthreaded image scraper for 500px.com')
    parser = argparse.ArgumentParser(description='Selenium based mutilthreaded image scraper for 500px.com')
    parser.add_argument('USER_NAME', type=str, help='username from 500px, must be exact')
    parser.add_argument('--MIN_WIDTH', type=int, help='Minimum width of the image to feteched', action='store', default='300')
    parser.add_argument('--MIN_HEIGHT', type=int, help='Minimum height of the image to feteched', action='store', default='300')
    parser.add_argument('--MAX_RECAPTURE_TIME', type=int, help='Max number of time to try to recapture', action='store', default='5')
    parser.add_argument('--INFINITE_SCROLL_LOAD_WAIT_TIME', type=int, help='Time in second that the infinite scroll function wait per scroll down motion that allow page to load', action='store', default='2')
    parser.add_argument('--INFINITE_SCROLL_END_CONFIRM_REDUN', type=int, help='usage refer to github page', action='store', default='2')
    parser.add_argument('--IMAGE_PAGE_LOAD_TIMEOUT', type=int, help='Time out in second used by the image fetecher, fetecher re-fectech the image after timed out', action='store', default='5')
    parser.add_argument('--PORTFOLIO_PAGE_LOAD_TIMEOUT', type=int, help='Time out in second used by the portfolio list fetecher, fetecher re-fectech the image list after timed out', action='store', default='10')
    parser.add_argument('--STUCK_REFRESH_INTERVAL', type=int, help='Time in second that the process wait when a page is unresponsive, i.e, passed the timeout value', action='store', default='3')
    parser.add_argument('--DEBUG_FLAG', type=bool, help='Toggle Verbose Debug Information Display', action='store', default=False)
    parser.add_argument('--SHOW_BROWSER', type=bool, help='Toggle browser visibility', action='store', default=False)
    parser.add_argument('--NUM_OF_THREAD', type=int, help='Number of thread used in the program', action='store', default='6')
    parser.add_argument('--IMAGE_FETCH_WAIT', type=int, help='Time in second the thread wait per fetecher process', action='store', default='2')
    return parser

parser = init_Parser()
args = parser.parse_args()

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

class InfoType(Enum):
    ERROR = 1
    DEBUG = 2
    INFO = 3

def printDebugInfo(infotag:InfoType, info:str, verbose=False):
    if verbose is False:
        if args.DEBUG_FLAG is False: return
    if infotag is InfoType.ERROR:
        print("[ERROR] " + info)
    elif infotag is InfoType.DEBUG:
        print("[DEBUG] " + info)
    elif infotag is InfoType.INFO:
        print("[INFO] " + info)

def initDirectory(username):
    dir = os.path.join(os.getcwd(), username)
    nsfwDir = os.path.join(dir, "NSFW")
    sfwDir = os.path.join(dir, "SFW")

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

    printDebugInfo(InfoType.INFO, "Found " + str(len(existingImgList)) + " Pre-existing Images", verbose=True)
    return sfwDir, nsfwDir

def getUrlListFromProfilePage(driver):
    infi_scroll_end_counter = 0
    imgPortfolio = WebDriverWait(driver, args.PORTFOLIO_PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div"))) # get element contain pictures from portfolio
    last_height = driver.execute_script("return document.body.scrollHeight")
    while infi_scroll_end_counter < args.INFINITE_SCROLL_END_CONFIRM_REDUN:
        printDebugInfo(InfoType.INFO, "Perform Scrolling Now", verbose=True)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(args.INFINITE_SCROLL_LOAD_WAIT_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            infi_scroll_end_counter += 1
        last_height = new_height

    printDebugInfo(InfoType.INFO, "Page End Reached!", verbose=True)
    portfolioElement = imgPortfolio.find_elements_by_tag_name('a')
    imgUrlsFromProfile = list({element.get_attribute('href') for element in portfolioElement if element.get_attribute('href') != None }) # get image page url
    return imgUrlsFromProfile

def fetechImgFromUrl(url:str, driver, existingImgList, sfwDir, nsfwDir, waittime):
    PassedQualityCheck = False
    printDebugInfo(InfoType.INFO, "Processing URL: " + url)
    component = re.match(r"https?:\/\/(.+?)(\/.*)", url)
    metaInfo = component[2].split('/')[1:]
    recaptureCount = 0
    successfullyCaptured = False
    if len(metaInfo) == 3:
        id500px = metaInfo[1]
        title = metaInfo[2]
        ifsfw = True

        if str(title + "_" + id500px + ".jpg") not in existingImgList:
            time.sleep(waittime)
            driver.get(url)
            # wait for the select element to become visible

            while (not PassedQualityCheck):
                try:
                    select_element = WebDriverWait(driver, args.IMAGE_PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]"))) #SFW content
                except:
                    printDebugInfo(InfoType.DEBUG, "!!Timed Out Expection!!")
                    driver.refresh()
                    time.sleep(args.STUCK_REFRESH_INTERVAL)
                    break

                if select_element.find_elements_by_tag_name('img') == []:
                    ifsfw = False # NSFW Content
                    try:
                        select_element = WebDriverWait(driver, args.IMAGE_PAGE_LOAD_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[3]"))) #NSFW content
                    except:
                        printDebugInfo(InfoType.DEBUG, "!!Timed Out Expection!!")
                        driver.refresh()
                        time.sleep(args.STUCK_REFRESH_INTERVAL)
                        break

                images = select_element.find_elements_by_tag_name('img')
                printDebugInfo(InfoType.DEBUG, "DEBUG! ----> " + str(images))

                for _, image in enumerate(images):
                    imgUrl = image.get_attribute('src')
                    printDebugInfo(InfoType.INFO, ">>>> Captured Img URL: " + imgUrl)
                    imgSize = getsizes(imgUrl)
                    imgSize = (0,0) if imgSize == None else imgSize # make sure the getsize function error get caught

                    if imgSize[0] > args.MIN_WIDTH and imgSize[1] > args.MIN_HEIGHT | recaptureCount > args.MAX_RECAPTURE_TIME:
                        printDebugInfo(InfoType.INFO, ">>>> Image Dimension: " + str(imgSize))
                        if recaptureCount > args.MAX_RECAPTURE_TIME:
                            printDebugInfo(InfoType.DEBUG, "Max Recapture Time Reached!!: ")
                            PassedQualityCheck = True

                        try:
                            if ifsfw:
                                request.urlretrieve(imgUrl, os.path.join(sfwDir, title + "_" + id500px + ".jpg"))
                            else:
                                request.urlretrieve(imgUrl, os.path.join(nsfwDir, title + "_" + id500px + ".jpg"))

                            PassedQualityCheck = True
                            successfullyCaptured = True
                        except:
                            printDebugInfo(InfoType.DEBUG, imgUrl + " URL INVALID!!", verbose = True)
                            recaptureCount +=1
                    else:
                        printDebugInfo(InfoType.INFO, ">>>> Quality Check Not Pass, Re-Capturing !!!!!")
                        recaptureCount += 1

            PassedQualityCheck = False
        else:
            printDebugInfo(InfoType.INFO, "Skiping " + title + "_" + id500px + ".jpg --- Already Exisit!")
            successfullyCaptured = True
    elif len(metaInfo) == 1:
        successfullyCaptured = True
    else:
        raise RuntimeError('[Error #1] Unexpected URL format, pls report This Bug on github!')
    return successfullyCaptured

def createDriver(showBroser):
    if args.SHOW_BROWSER:
        mydriver = webdriver.Firefox()
    else:
        options = Options()
        options.add_argument('--headless')
        mydriver = webdriver.Firefox(options=options)
    return mydriver

def newImgCaptureBrowserThread(pid, subUrlList, existingImgList, sfwDir, nsfwDir, waittime, showBroser):
    successfulImgCaptureCount = 0
    failedCaptureImageURLList = []
    mydriver = createDriver(showBroser)
    for url in tqdm(subUrlList, desc="PID# "+str(pid)):
        if fetechImgFromUrl(url, mydriver, existingImgList, sfwDir, nsfwDir, waittime):
            successfulImgCaptureCount += 1
        else:
            failedCaptureImageURLList.append(url)

    mydriver.quit()
    printDebugInfo(InfoType.INFO, "[PID# " + str(pid) + "] CapturedImgCount: " + str(successfulImgCaptureCount) + " FailedImgURL List: " + str(failedCaptureImageURLList), verbose=True)


existingImgList = []
sfwDir, nsfwDir = initDirectory(args.USER_NAME)

mydriver = createDriver(args.SHOW_BROWSER)

mydriver.get('https://500px.com/' + args.USER_NAME)
urlListFromProfilePage = getUrlListFromProfilePage(mydriver)
mydriver.quit()

process_list = []
urlListLength = len(urlListFromProfilePage)
subListlen = int(urlListLength / args.NUM_OF_THREAD)
for i in range(args.NUM_OF_THREAD):
    if i+1 == args.NUM_OF_THREAD: #end of the list
        subURLlist = urlListFromProfilePage[subListlen*i:]
    else:
        subURLlist = urlListFromProfilePage[subListlen*i:subListlen*(i+1)]
    process = threading.Thread(name='Test {}'.format(i), target=newImgCaptureBrowserThread, args=(i,subURLlist,existingImgList, sfwDir, nsfwDir, args.IMAGE_FETCH_WAIT, args.SHOW_BROWSER))
    process.start()
    time.sleep(1)
    printDebugInfo(InfoType.INFO, "Muti Thread Process Initiated", verbose=False)
    process_list.append(process)

# Wait for all thre<ads to complete
for thread in process_list:
    thread.join()

print("\n Job Complete, Created by Chengming Kevin Zhang 2020 \n")
