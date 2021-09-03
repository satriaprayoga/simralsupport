from simral import input_dpa_perubahan as idp
from simral import simral_login as sl

from selenium import webdriver

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-09-30)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Dalam APBDP"

import logging

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
    
sl.login(driver,USERNAME,PASSWORD,CFG,captcha_code)
idp.modul_belanja_dppa(driver)
links=idp.pilih_skpd(driver,PERIODE,'[5.02.0.00.0.00.01.0000] BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH','[5.02.0.00.0.00.01.0004] Bidang Akutansi dan Teknologi Informasi')
print("{} kegiatan".format(len(links)))
for l in links:
    print(l)


rincians=idp.pilih_sub_kegiatan(driver,links[0])
print("{} sub-kegiatan".format(len(rincians)))

for r in rincians:
    print(r)
