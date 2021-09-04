import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as NSEE
from selenium.webdriver.common.by import By

windows = 1
completed = 0
check_delay = 1
#all percentages below
like_chance = 40
scroll_amount = 20

def watch(url):
    global windows
    global completed
    global check_delay
    global like_chance
    global scroll_amount
    element = None

    options = Options()
    options.add_argument("--mute-audio")
    options.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)

    driver.get(url)
    drop_down = True
    try:
        print('Waiting for drop down... (1)')
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "onesignal-slidedown-cancel-button"))
        )
        later = driver.find_element_by_xpath('/html/body/div[12]/div/div/div[2]/button[2]')
        later.click()
        drop_down = False
        print('Drop down removed')
    except:
        print('Drop down cancelled')

    #click sign in button
    element = driver.find_element_by_xpath("/html/body/div[3]/div[2]/a[2]")
    element.click()

    #put email address
    element = driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[2]/form/div[1]/input')
    element.clear()
    element.send_keys("EMAIL")

    #put password
    element = driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[2]/form/div[2]/input')
    element.clear()
    element.send_keys("PASS")

    #confirms information to sign in
    element = driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[2]/form/div[4]/button')
    element.click()

    print('---------------Logged In!---------------')

    if drop_down:
        try:
            print('Waiting for drop down... (2)')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "onesignal-slidedown-cancel-button"))
            )
            later = driver.find_element_by_xpath('/html/body/div[12]/div/div/div[2]/button[2]')
            later.click()
            print('Drop down removed')
        except:
            print('Drop down cancelled')

    def click_first_video():
        video = driver.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/div[1]/div/a/div')
        video.click()

    print('Opening ({}) windows...'.format(windows))
    for window in range(windows - 1): driver.execute_script("window.open('{}', 'MyWindow{}', 'location=no,status=no');".format(url, window))
    print('Windows have been opened')

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NSEE:
            return False
        return True

    def check_exists_by_class_name(xpath):
        try:
            driver.find_element_by_class_name(xpath)
        except NSEE:
            return False
        return True

    #iterate through windows
    i = 1
    window_titles = {}
    for window in driver.window_handles:
        window_titles[i] = driver.current_url
        try:
            print('Waiting for video to load...')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div/div[1]/div[1]/a/div"))
            )
            element = driver.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/div[1]/a/div')
            element.click()
            print('done!')
        except:
            print('Exceeded timeout for video load time. There may have been an advertisement at the beginning.')
        i += 1

    #iterate through windows to perform routine checks
    while True:
        i = 1
        for window in driver.window_handles:
            try:
                if window_titles[i] != driver.current_url:
                    window_titles[i] = driver.current_url
                    #check if like button
                    if random.random() * 100 <= like_chance:
                        if check_exists_by_xpath('/html/body/div[8]/div[1]/div[2]/div[4]/div[1]/div/button'):
                            element = driver.find_element_by_xpath('/html/body/div[8]/div[1]/div[2]/div[4]/div[1]/div/button')
                            element.click()
                            print('Liked video (url: {})!'.format(driver.current_url))

                    time.sleep(random.random() * 3)
                    scheight = .1
                    while scheight < 9.9 + scroll_amount * random.random():
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
                        scheight += .05
                    driver.execute_script("window.scrollTo(0, 0);")

                    print('New video has been loaded (Name: {})'.format(driver.title))


                #ad skip scripts don't work for some reason
                if check_exists_by_xpath('/html/body/div/div[4]/div[2]/button'):
                    element = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/button')
                    element.click()
                    print('Ad skipped!')
                if check_exists_by_xpath('/html/body/div/div[4]/div[2]/button/div[1]'):
                    element = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/button/div[1]')
                    element.click()
                    print('Ad skipped!')
                if check_exists_by_class_name('videoAdUiSkipButton videoAdUiAction videoAdUiRedesignedSkipButton'):
                    element = driver.find_element_by_class_name('videoAdUiSkipButton videoAdUiAction videoAdUiRedesignedSkipButton')
                    element.click()
                    print('Ad skipped!')
                if check_exists_by_class_name('videoAdUiSkipButtonExperimentalText'):
                    element = driver.find_element_by_class_name('videoAdUiSkipButtonExperimentalText')
                    element.click()
                    print('Ad skipped!')

                if random.random() * 100 < 10:
                    scheight = .1
                    while scheight < 9.9 + scroll_amount * random.random():
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
                        scheight += .05
                    driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(check_delay)
                i += 1
            except:
                print('error')
    # avoid c++ garbage collection
    return driver


#skip ad xpath: /html/body/div/div[4]/div[2]/button
#skip ad class_name: videoAdUiSkipButton videoAdUiAction videoAdUiRedesignedSkipButton
#text skip xpath: /html/body/div/div[4]/div[2]/button/div[1]
#text skip name: videoAdUiSkipButtonExperimentalText
url = 'https://hideout.co/'
driver = watch(url)
