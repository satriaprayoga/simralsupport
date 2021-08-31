from simral import input_dpa_perubahan as idp
from simral import simral_login as sl

from selenium import webdriver

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-08-31)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Dalam APBDP"

import logging
import time

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
#modul_perubahan(driver)
#pilih_kegiatan(driver,PERIODE,'[1.05.0.00.0.00.01.0000] SATUAN POLISI PAMONG PRAJA','[1.05.0.00.0.00.01.0001] Sekretariat Sat Pol PP')
#import_kegiatan(driver,JENIS_PERUBAHAN)
print("{} kegiatan".format(len(links)))
for l in links:
    print(l)

rincians=idp.pilih_sub_kegiatan(driver,links[0])
print("{} sub-kegiatan".format(len(rincians)))

for r in rincians:
    print(r)
rekening=idp.pilih_rincian_anggaran(driver,rincians[0])
print("{} rekening".format(len(rekening)))
for rek in rekening:
    print(rek)

idp.edit_rincian_anggaran(driver,rekening[0].get('link'))