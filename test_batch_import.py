from simral_import_apbd_p import import_kegiatan, modul_perubahan, pilih_kegiatan
from selenium import webdriver
from simral_login import  *

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="Perubahan Reguler (2021-08-30 s/d 2021-11-01)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Dalam APBDP"

import logging
import time
import csv

f=open('subunit.csv',"r")
csv_content=csv.DictReader(f)


logging.basicConfig(level=logging.INFO)
driver=webdriver.Chrome(r'./chromedriver.exe')
connect_to_simral(driver)
find_captcha(driver)
print("Masukkan kode CAPTCHA:")
captcha_code=input()

if(captcha_code.isdigit()==False):
    logging.error("Format CAPTCHA salah (0-9)!")
    driver.quit()
    exit(-1)
    
login(driver,USERNAME,PASSWORD,CFG,captcha_code)
for row in csv_content:
    skpd="[{}] {}".format(row['kode_skpd'],row['nama_skpd'])
    sub_skpd="[{}] {}".format(row['kode_sub_skpd'],row['nama_sub_skpd'])
    modul_perubahan(driver)
    pilih_kegiatan(driver, PERIODE, skpd, sub_skpd)
    import_kegiatan(driver, JENIS_PERUBAHAN)

f.close()
#modul_perubahan(driver)
#pilih_kegiatan(driver,PERIODE,'[1.05.0.00.0.00.01.0000] SATUAN POLISI PAMONG PRAJA','[1.05.0.00.0.00.01.0001] Sekretariat Sat Pol PP')
#import_kegiatan(driver,JENIS_PERUBAHAN)
time.sleep(2)