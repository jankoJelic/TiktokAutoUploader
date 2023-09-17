from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common
import time

class Bot:
    """Bot used as high level interaction with web-browser via Javascript exec"""
    def __init__(self, bot):
        self.bot = bot

    def getBot(self):
        return self.bot

    def getVideoUploadInput(self):
        # Button is nested in iframe document. Select iframe first then select upload button
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        time.sleep(4)
        iframe = self.bot.find_element(By.TAG_NAME, "iframe")
        self.bot.switch_to.frame(iframe)
        self.bot.implicitly_wait(2)
        time.sleep(5)
        self.bot.execute_script("document.querySelectorAll('iframe')[0]?.contentDocument.body.querySelector('input').setAttribute('style', 'display:flex;')")
        file_input_element = self.bot.find_element(By.TAG_NAME, "input")
        return file_input_element

    def getCaptionElem(self):
        self.bot.implicitly_wait(3)
        self.bot.execute_script(
            f'var element = document.getElementsByClassName("public-DraftStyleDefault-block")[0].children['
            f'0].getAttribute("data-offset-key");')
        caption_elem = self.bot.find_elements(By.CLASS_NAME, "public-DraftStyleDefault-block")[0]
        return caption_elem

    def selectPrivateRadio(self):
        try:
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "permission")))
            open_menu = self.bot.find_elements(By.CLASS_NAME, "permission")[0].find_elements(By.XPATH, './*')[1].find_elements(By.XPATH, './*')[0]
            open_menu.click()
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tiktok-select-dropdown-item")))
            self.bot.find_elements(By.CLASS_NAME, "tiktok-select-dropdown-item")[2].click()

        except Exception as e:
            print(f"Private Toggle Error: {e}")
            self.click_elem(
                # 'document.getElementsByClassName("radio-group")[0].children[2].click()',
                "document.getElementsByClassName('permission')[0].childNodes[1].childNodes[2].click()",
                "Javascript had trouble finding the 'private' toggle radio button with given selector,"
                " please submit yourself and edit submit button placement.!!")


    def selectPublicRadio(self):
        # Button Works
        try:
            WebDriverWait(self.bot, 10).until(EC.presence_of_element_located(self.bot.find_elements_by_class_name("permission")[0].childNodes[1].childNodes[0]))
            open_menu = self.bot.find_elements_by_class_name("permission")[0].childNodes[1].childNodes[0].click()
            WebDriverWait(self.bot, 10).until(EC.presence_of_element_located(self.bot.find_elements_by_class_name("tiktok-select-dropdown")[0].childNodes[0]))
            public_submenu = self.bot.find_elements(By.CLASS_NAME, "tiktok-select-dropdown")[0].childNodes[0]
            # Needs to be done in action chain to work.

        except Exception as e:
            self.click_elem(
                # 'document.getElementsByClassName("radio-group")[0].children[0].click()',
                "document.getElementsByClassName('permission')[0].childNodes[1].childNodes[0].click()",
                "Javascript had trouble finding the 'public' toggle radio button with given selector,"
                " please submit yourself and edit submit button placement.!!")


    def selectScheduleToggle(self):
    # deprecated function
        self.click_elem(
            "document.getElementsByClassName('switch-container')[0].click()",
            "Javascript had trouble finding the 'schedule' toggle radio button with given selector,"
            " please submit yourself and edit submit button placement.!!")

    def uploadButtonClick(self):
        time.sleep(6)
        post_button_xpath = '//div[text()="Post"]'
        WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.XPATH, post_button_xpath)))
        time.sleep(12)
        self.bot.execute_script("document.body.querySelector('div[class*=btn-post]').querySelector('button').click()")
        WebDriverWait(self.bot, 30).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Upload another video"]')))
        time.sleep(3)
        self.bot.quit()
     
    def click_elem(self, javascript_script, error_msg):
        try:
            self.bot.execute_script(javascript_script)
        except selenium.common.exceptions.JavascriptException as je:
            print(error_msg)
            print(je)
        except Exception as e:
            print(f"Unhandled Error: {e}")
            exit()
        return