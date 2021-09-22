from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotVisibleException, NoSuchElementException, TimeoutException
import logging
import base64
import io
from PIL import Image


class SimralDriver:

    __simral_url="https://simral.bogorkab.go.id/2021"

    __navElement="nav"
    __moduleMenu="SelectModul"

    def __init__(self):
        self._driver=None

    def connect(self,chromeLocation,headless=False,width=1920,height=1080):
        try:
            # options =webdriver.ChromeOptions()
            
            # if headless==True:
            #     options.add_argument("--headless") # Runs Chrome in headless mode.
            #     options.add_argument('--no-sandbox') # Bypass OS security model
            #     options.add_argument('--disable-gpu')  # applicable to windows os only
            #     options.add_argument('start-maximized') # 
            #     options.add_argument(f'window-size={width}x{height}')
            #     options.add_argument('disable-infobars')
            #     options.add_argument("--disable-extensions")
            # else:
            #     options.add_argument('disable-infobars')
            #     options.add_argument('start-maximized') # 
            #     options.add_argument(f'window-size={width}x{height}')
           
            logging.info("Memulai koneksi ke {}".format(self.__simral_url))
            self._driver=webdriver.Chrome(chromeLocation)
            self._driver.set_window_size(width,height)

           
            self._driver.get(self.__simral_url)
            WebDriverWait(self._driver,5).until(EC.title_is('SIMRAL'))
        except Exception as err:
            logging.error(err)

    
    def get_captcha(self):
        try:
            logging.info("Mencari element CAPTCHA untuk authentifikasi")
            captchaTag=WebDriverWait(self._driver,1).until(EC.presence_of_element_located((By.ID,"captcha")))
            img_base64 = self._driver.execute_script("""
        var ele = arguments[0];
        var cnv = document.createElement('canvas');
        cnv.width = 100; cnv.height = 40;
        cnv.getContext('2d').drawImage(ele, 0, 0);
        return cnv.toDataURL('image/jpeg').substring(22);    
        """, captchaTag)   #"/html/body/form/div[2]/div[3]/span[3]/div[1]/img"))
            binary=base64.b64decode(img_base64)
            file_like=io.BytesIO(binary)
            img=Image.open(file_like)
        # img.save('captcha.png')
            #image=Image.open('captcha.png')
            img.show()
        except Exception as err:
            logging.error("Element CAPTCHA tidak ditemukan {}".format(err))
        finally:
            img.close()
    
    def login(self,user,password,cfg,captcha_code):
        try:
            self._driver.find_element_by_name('nama_login').send_keys(user)
            self._driver.find_element_by_name('password').send_keys(password)
            Select(self._driver.find_element_by_id("lived_cfg")).select_by_visible_text(cfg)
            self._driver.find_element_by_id('captcha_code').send_keys(captcha_code)
            self._driver.implicitly_wait(1)
            self._driver.find_element_by_name("login").submit()
            
        except TimeoutException:
            logging.error("Request Time Out. Tidak ada Respoonse : %s",self.__simral_url)
            self._driver.quit()
        except NoSuchElementException:
            logging.error("Element CAPTCHA tidak ditemukan")
            self._driver.quit()
        except ElementClickInterceptedException:
            logging.error("Login gagal")
            self._driver.quit()

    def get_driver(self):
        return self._driver

    def quit_driver(self):
        self._driver.quit()

    def select_modul(self,moduleName,linkNode):
        try:
            logging.info(f'Memilih modul : {moduleName}')
            self._driver.switch_to.frame(self._driver.find_element_by_name(self.__navElement))
            moduleMenu=self._driver.find_element_by_id(self.__moduleMenu)
            Select(moduleMenu).select_by_visible_text(moduleName)

            self._driver.execute_script(f' document.getElementById("{linkNode}").style.display = "inline"')
            self._driver.find_element_by_xpath("//div[@id='{}']//nobr//a".format(linkNode)).click()
            self._driver.switch_to.default_content()
       
        except Exception as err:
            logging.error(err)

    def select_modul_by_name(self,moduleName,linkName):
        try:
            logging.info(f'Memilih modul : {moduleName}')
            self._driver.switch_to.frame(self._driver.find_element_by_name(self.__navElement))
            moduleMenu=self._driver.find_element_by_id(self.__moduleMenu)
            Select(moduleMenu).select_by_visible_text(moduleName)

            self._driver.execute_script("""
             var links=document.getElementsByClassName("treemenu")
             for(i=0;i<links.length;i++){
                 links[i].style.display = "inline"
             }
             """)
            #self._driver.find_element_by_xpath("//div[@id='{}']//nobr//a".format(linkNode)).click()
            self._driver.implicitly_wait(2)
            self._driver.find_element_by_partial_link_text(linkName).click()
            self._driver.switch_to.default_content()
       
        except Exception as err:
            logging.error(err)

    def switchFrame(self,frameName,timeout=1):
        try:
            WebDriverWait(self._driver,timeout).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,frameName)))
        except Exception as err:
            logging.error(err)

    def switchToDefault(self):
        self._driver.switch_to.default_content()

    
