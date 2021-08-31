from selenium import webdriver
from simral import import_dpa_perubahan as idp
from simral import simral_login as sl
from simral import settings


import logging
import time
import csv

f=open('subunit.csv',"r")
csv_content=csv.DictReader(f)


logging.basicConfig(level=logging.INFO)
driver=webdriver.Chrome(r'./chromedriver.exe')
sl.connect_to_simral(driver)
sl.find_captcha(driver)
print("Masukkan kode CAPTCHA:")
captcha_code=input()

if(captcha_code.isdigit()==False):
    logging.error("Format CAPTCHA salah (0-9)!")
    driver.quit()
    exit(-1)
    
sl.login(driver,settings.USERNAME,settings.PASSWORD,settings.CFG,captcha_code)
for row in csv_content:
    skpd="[{}] {}".format(row['kode_skpd'],row['nama_skpd'])
    sub_skpd="[{}] {}".format(row['kode_sub_skpd'],row['nama_sub_skpd'])
    idp.modul_perubahan(driver)
    idp.pilih_kegiatan(driver, settings.PERIODE, skpd, sub_skpd)
    idp.import_kegiatan(driver, settings.JENIS_PERUBAHAN)

f.close()
time.sleep(2)
driver.quit()