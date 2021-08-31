from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotVisibleException, NoSuchElementException, TimeoutException
import logging
import base64
import io
import time
from PIL import Image

SIMRAL_2021_URL="https://simral.bogorkab.go.id/2021"

def connect_to_simral(driver):
    try:
        driver.get(SIMRAL_2021_URL)
        logging.info("Memulai koneksi ke: %s ",SIMRAL_2021_URL)
        WebDriverWait(driver,5).until(EC.title_is('SIMRAL'))
        
    except TimeoutException:
        logging.error("Request Time Out. Tidak ada Respoonse : %s",SIMRAL_2021_URL)

def find_captcha(driver):
    try:
        logging.info("Mencari element CAPTCHA untuk authentifikasi")
        captchaTag=WebDriverWait(driver,1).until(EC.presence_of_element_located((By.ID,"captcha")))
        captchaImg=captchaTag.get_attribute("src")
        img_base64 = driver.execute_script("""
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
    except TimeoutException:
        logging.error("Request Time Out. Tidak ada Respoonse : %s",SIMRAL_2021_URL)
    except NoSuchElementException:
        logging.error("Element CAPTCHA tidak ditemukan")
    finally:
        img.close()

def login(driver,user,password,cfg,captcha_code):
    try:
        driver.find_element_by_name('nama_login').send_keys(user)
        driver.find_element_by_name('password').send_keys(password)
        Select(driver.find_element_by_id("lived_cfg")).select_by_visible_text(cfg)
        driver.find_element_by_id('captcha_code').send_keys(captcha_code)
        time.sleep(1)
        driver.find_element_by_name("login").submit()

    except TimeoutException:
        logging.error("Request Time Out. Tidak ada Respoonse : %s",SIMRAL_2021_URL)
        driver.quit()
    except NoSuchElementException:
        logging.error("Element CAPTCHA tidak ditemukan")
        driver.quit()
    except ElementClickInterceptedException:
        logging.error("Login gagal")
        driver.quit()