from simral import simral_login
from simral import input_dpa_perubahan as idp
from simral import settings
from selenium import webdriver


import logging
import time
import json
import os

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-09-30)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Anggaran Sebelum APBD-P"

logging.basicConfig(level=logging.INFO)

def loadDataSkpd():
    try:
        logging.info("Membuka referensi data ")
        f=open('dpa.json',"r")
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

def loadDpa(skpd):
    f=open(f'referensi/{skpd}.json','r')
    jsonData=json.load(f)
    f.close()
    return jsonData

def extractDataRincianFromDpa(dpa):
    path=f'referensi/temp'
    isExist=os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    for d in dpa:
        rincian_objek=d['rincian_objek']
        rincian=[]
        for rek in rincian_objek:
            rincian.append({"kode_giat":d['kode_giat'],"nama_giat":d['nama_giat'],"kode_sub_giat":d['kode_sub_giat'],"nama_sub_giat":d['nama_sub_giat'],"kode_akun":rek['kode_akun'],"nama_akun":rek['nama_akun'],"total_rincian":rek['total_rincian']})
            #rincian.append({"kode_akun":rincian_objek['kode_akun'],"nama_akun":rincian_objek['nama_akun'],"total_rincian":rincian_objek['total_rincian']})
            json_object=json.dumps(rincian,indent=2,sort_keys='kode_akun')
            f=open(f'referensi/temp/{d["kode_program"]}-{d["kode_giat"]}-{d["kode_sub_giat"]}-{rek["kode_akun"]}','w')
            f.write(json_object)
            f.close()

skpdList=loadDataSkpd()
print(skpdList)
skpd=pilihSkpd(skpdList)



# for d in dpa:
#     print(f'{d["nama_giat"]}:{d["nama_sub_giat"]}')
# driver=webdriver.Chrome(r'./chromedriver.exe')
# driver.maximize_window()
# simral_login.connect_to_simral(driver)
# simral_login.find_captcha(driver)

# print(f'Masukkan kode CAPTCHA: ')
# captcha=input()

# if not captcha.isdigit():
#     logging.error("Format CAPTCHA salah!")
#     driver.quit()
#     exit(-1)

# simral_login.login(driver, USERNAME, PASSWORD, CFG, captcha)
# idp.modul_belanja_dppa(driver)
# kegiatan_list=idp.pilih_kegiatan(driver,PERIODE,'[5.02.0.00.0.00.01.0000] BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH','[5.02.0.00.0.00.01.0004] Bidang Akutansi dan Teknologi Informasi','[5.02] KEUANGAN','[5.02.02] PROGRAM PENGELOLAAN KEUANGAN DAERAH')
# print(kegiatan_list)cv
# for d in dpa:
#     idp.modul_belanja_dppa(driver)
#     kode_skpd=d['kode_skpd']
#     nama_skpd=d['nama_skpd']
#     kode_sub_skpd=d['kode_sub_skpd']
#     nama_sub_skpd=d['nama_sub_skpd']
#     kode_bidang_urusan=d['kode_bidang_urusan']
#     nama_bidang_urusan=d['nama_bidang_urusan']
#     kode_program=d['kode_program']
#     nama_program=d['nama_program']

#     if nama_sub_skpd!=nama_skpd:
#         link_kegiatans=idp.pilih_kegiatan(driver,PERIODE,f'[{kode_skpd}] {nama_skpd}',f'[{kode_sub_skpd}] {nama_sub_skpd}', f'[{kode_bidang_urusan}] {nama_bidang_urusan}', f'[{kode_program}] {nama_program}')
#         if(link_kegiatans):
#             for ls in link_kegiatans:
#                 link_subs=idp.pilih_sub_kegiatan(driver, ls)
#                 for l in link_subs:
#                     link_rincians=idp.pilih_rincian_anggaran(driver,l)
                   
#         else:
#             print('Tidak ada kegiatan')
