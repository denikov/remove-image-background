import os
import time

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from opencv import OpenCV
import services


class Browser:

    def __init__(self):

        self._opencv = OpenCV()

        #PROXY = '118.175.93.148:54094'
        #PROXY = '180.131.52.194:11002'

        chrome_options = Options()
        cwd = os.getcwd()
        prefs = {'download.default_directory': os.path.join(cwd, './remove-image-background/temp')}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

        #chrome_options.add_argument('--proxy-server=%s' % PROXY)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get('https://www.google.com')
        self.driver.execute_script("window.open('https://www.remove.bg', '_blank');")
        time.sleep(1)
        self.driver.switch_to_window(self.driver.window_handles[0])



    def close(self):
        self.driver.quit()
        exit()



    def removebg(self, href):
        wait = WebDriverWait(self.driver, 20)

        time.sleep(1)
        self.driver.find_element_by_class_name('select-photo-url-btn').click()
        try:
            alert = wait.until(EC.alert_is_present(), 'Timed out waiting for alerts to appear')
            alert = self.driver.switch_to.alert
            time.sleep(2)
# the prompt box will not show keys entered but the value does change
            alert.send_keys(href)
            time.sleep(2)
            alert.accept()
        except TimeoutException:
            self.driver.execute_script("window.alert('Prompt box did not appear, close this browser and restart');")
            time.sleep(3)
            print('timeout: no prompt appeared')
            self.close()
            return

        try:
            processedImage = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class*="transparency-grid"]')))
            time.sleep(4)
            self.driver.find_element_by_css_selector('a[href*="o.remove.bg/download"]').click()
            time.sleep(2)
            self.driver.find_element_by_class_name('image-result--delete-btn').click()
            time.sleep(1)
            self.driver.execute_script("window.scrollTo({top:0, behavior:'smooth'})")
            time.sleep(1)
            self.driver.switch_to_window(self.driver.window_handles[0])
            imageFileName = self._opencv.processDownloadedImage(services._name_list[services._current_index]['name'])

# finish here, go to next person of interest
            if imageFileName is not None:
# save new image file name and continue to next
                nextName = services.addToJSON(imageFileName)
                if nextName is not None:
                    self.search(nextName)
                    self.previewIsSelected()
                else:
                    self.close()

            else:
                time.sleep(1)
                self.driver.execute_script("window.alert('No face found or picture not accessable. Please select another one');")
                time.sleep(1)
                self.previewIsSelected()
                return

        except TimeoutException:
            print('timed out on image processing')
            try:
# check for alert div
                self.driver.find_element_by_class_name('alert')
            except:
# alert missing, waiting too long for image
                time.sleep(1)
                self.driver.execute_script("window.scrollTo({top:0, behavior:'smooth'})")
                self.driver.switch_to_window(self.driver.window_handles[0])
                time.sleep(1)
                self.driver.execute_script("window.alert('Remove.bg could not distinguish background.  Choose another image.');")
                self.previewIsSelected()
            else:
                try:
                    self.driver.find_element_by_class_name('delete-image-btn').click()
                except:
                    pass
                time.sleep(1)
                self.driver.execute_script("window.scrollTo({top:0, behavior:'smooth'})")
                self.driver.switch_to_window(self.driver.window_handles[0])
                time.sleep(1)
                self.driver.execute_script("window.alert('');")
                self.previewIsSelected()



    def previewIsSelected(self):
        try:
# check if alert with a message is opened
            self.driver.switch_to.alert
        except:
            pass
        else:
            time.sleep(3)
            self.previewIsSelected()
            return

# check if preview window is opened
        wait = WebDriverWait(self.driver, 60)
        try:
            opened = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'irc-vo')))
        except TimeoutException:
            self.previewIsSelected()
            return
        else:
            element = None
            href = None
# find correct preview div which does not have display:none
            for div in self.driver.find_elements_by_class_name('irc_c'):
                if div.value_of_css_property('display') != 'none':
                    element = div
                    break

            if element is not None:
# check image size
                width = self.driver.execute_script("var x=document.querySelectorAll('div.irc_c'),idx;for(var i=0; i<x.length; i++){if(x[i].style.display !== 'none'){idx=x[i].querySelector('span.irc_idim').textContent;break;}}return idx;")
                width = width.split(' ')[0]
                if int(width) < 300:
                    self.driver.find_element_by_id('irc_ccbc').click()
                    self.driver.execute_script("window.alert('This image is pretty small.  For better results, find one above 300px.');")
                    time.sleep(2)
                    self.previewIsSelected()
                    return
                else:
                    href = element.find_elements_by_tag_name('img')[0].get_attribute('src')
                    time.sleep(1)
                    self.driver.find_element_by_id('irc_ccbc').click()
            else:
                print('element containing an image not found')

            if href is not None:
# check if face found on selected image
                faceFound = self._opencv.checkForFaces(href)
                if faceFound is not None:
                    self.driver.execute_script("window.scrollTo({top:0, behavior:'smooth'})")
# switch to remove.bg
                    self.driver.switch_to_window(self.driver.window_handles[1])
                    time.sleep(1)
                    self.removebg(href)
                else:
# face not found, send alert to browser, wait for another picture to be selected
                    self.driver.execute_script("window.alert('No face found or picture not accessable. Please select another one');")
                    self.previewIsSelected()



    def search(self, name):
        if name is None:
            self.browser.quit()
            exit()
        else:
# google search
# check for search input field
            if self.driver.find_element_by_css_selector('input.gLFyf.gsfi'):
# fill out input
                self.driver.find_element_by_name('q').clear()
                time.sleep(1)
                self.driver.find_element_by_name('q').send_keys(name)
                time.sleep(1)

# check if on a page with results, find search icon
                try:
                    self.driver.find_element_by_css_selector('button.Tg7LZd').click()
                except:
# on google.com home page button
                    self.driver.execute_script("document.getElementsByName('btnK')[0].click();")

            else:
# could be loading...allow to load here
                time.sleep(3)
                self.search(self, name)

            time.sleep(2)
# find nav bar
            tabs = self.driver.find_elements_by_class_name('hdtb-mitem')
            if tabs[1].get_attribute('aria-selected') == 'false':
                tabs[1].find_element_by_tag_name('a').click()
                #driver.execute_script("var tabs = document.querySelectorAll('div.hdtb-mitem');if(tabs[1].querySelector('a'))tabs[1].querySelector('a').click();")
                print('Select an image which contains just the person of interest alone. You can modify the search parameters.')
            return

