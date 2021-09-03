from simral import simral_login
from simral import import_dpa_perubahan as idp
from simral import settings
from selenium import webdriver


import logging
import time
import json

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-09-30)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Anggaran Sebelum APBD-P"

logging.basicConfig(level=logging.INFO)

def loadDataSkpd():
    try:
        logging.info("Membuka referensi data ")
        f=open('referensi/unit.json',"r")
        jsonData=json.load(f)
        return jsonData
    except Exception as e:
        logging.error(e)
    finally:
        f.close()

def pilihSkpd(jsonData):
    for data in jsonData:
        print(f"{data['id_skpd']} {data['nama_skpd']}")
    print("Pilih ID SKPD yang akan di Import ke SIMRAL (contoh: untuk memilih DINAS PENDIDIKAN, ketik 1367)")
    id_skpd=input()
    skpd=None
    if id_skpd.isdigit():
        for data in jsonData:
            if data['id_skpd']==int(id_skpd):
                skpd=data
                break
    else:
        logging.error("format ID SKPD salah")
        return -1
    return skpd

""" driver = webdriver.Chrome(r'./chromedriver.exe')
simral_login.connect_to_simral(driver)
simral_login.find_captcha(driver)
print("Masukkan kode captcha: ")
captcha=input()

if not captcha.isdigit():
    logging.error("Format CAPTCHA salah (0-9)!")
    driver.quit()
    exit(-1) """


skpdList=loadDataSkpd()
skpd=pilihSkpd(skpdList)
logging.info("Import {} ke SIMRAL".format(skpd['nama_skpd']))
driver = webdriver.Chrome(r'./chromedriver.exe')
simral_login.connect_to_simral(driver)
simral_login.find_captcha(driver)
print("Masukkan kode captcha: ")
captcha=input()

if not captcha.isdigit():
    logging.error("Format CAPTCHA salah!")
    driver.quit()
    exit(-1)

simral_login.login(driver, USERNAME, PASSWORD, CFG, captcha)

logging.info(f'Import DPA [{skpd["kode_skpd"]}] {skpd["nama_skpd"]}')
print('Unit SKPD:')
for unit in skpd["sub_skpd"]:
    start=time.perf_counter()
    idp.modul_perubahan(driver)
    print(f'Import Kegiatan pada [{unit["kode_sub_skpd"]}] {unit["nama_sub_skpd"]}')
    idp.pilih_kegiatan(driver, PERIODE, f'[{skpd["kode_skpd"]}] {skpd["nama_skpd"]}', f'[{unit["kode_sub_skpd"]}] {unit["nama_sub_skpd"]}')
    idp.import_kegiatan(driver, JENIS_PERUBAHAN)
    end=time.perf_counter()
    time.sleep(1)
    print(f"Execution Time : {end - start:0.6f} seconds" )
driver.quit()