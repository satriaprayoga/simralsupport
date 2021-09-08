from simral import simral_login
from simral import input_dpa_perubahan as idp
from simral import settings
from simral.sipd.Backup import *

from selenium import webdriver


import logging
import time
import json
import os
import sqlite3

USERNAME="gilang_2021"
PASSWORD="1234567a"
PERIODE="PARSIAL 3 (2021-07-13 s/d 2021-09-30)"
CFG="2021"
JENIS_PERUBAHAN="Perubahan Anggaran Sebelum APBD-P"

logging.basicConfig(level=logging.INFO)

conn=sqlite3.connect('sipd_backup.db')

def load_skpd():
    try:
        skpd_list=findAllSkpd(conn)
        return skpd_list
    except Exception as err:
        print(err)


skpdList=load_skpd()
for skpd in skpdList:
    print(f'{skpd["id_skpd"]} {skpd["nama_skpd"]}')

print("Pilih ID SKPD yang akan di Import ke SIMRAL (contoh: untuk memilih DINAS PENDIDIKAN, ketik 1367)")
id_skpd=input()
skpd=findSkpdById(conn,id_skpd)
if skpd:
    print("Anda Memilih : {}".format(skpd['nama_skpd']))
else:
    print("SKPD tidak ditemukan")
    exit(0)


driver = webdriver.Chrome(r'./chromedriver.exe')
#driver.maximize_window()
driver.set_window_size(1250,700)
simral_login.connect_to_simral(driver)
simral_login.find_captcha(driver)

print("Masukkan kode captcha")
captcha=input()

if not captcha.isdigit():
    logging.error("Format CAPTCHA salah!")
    driver.quit()
    exit(-1)

simral_login.login(driver, USERNAME, PASSWORD, CFG, captcha)
idp.modul_belanja_dppa(driver)

program_fields=findProgramFromIdSkpd(conn, skpd['id_skpd'])

for field in program_fields:
    link_kegiatans=idp.list_kegiatan(driver,PERIODE,f'[{field["kode_skpd"]}] {field["nama_skpd"]}', f'[{field["kode_sub_skpd"]}] {field["nama_sub_skpd"]}', f'[{field["kode_bidang_urusan"]}] {field["nama_bidang_urusan"]}', f'[{field["kode_program"]}] {field["nama_program"]}')
    kegiatans=findKegiatan(conn, field["kode_skpd"],field["kode_sub_skpd"],field["kode_bidang_urusan"], field["kode_program"])
    for l,k in zip(link_kegiatans,kegiatans):
        if l['idKgtn']==k['kode_giat']:
            ## ke halaman sub kegiatan untuk kegiatan 'kode_skpd'
            idp.choose_kegiatan(driver,k,l['link'],False) #False for action
            subs=findSubkegiatan(conn,k["kode_skpd"],k["kode_sub_skpd"],k["kode_bidang_urusan"], k["kode_program"],k["kode_giat"])
            link_subs=idp.list_sub_kegiatan(driver,False)
            # for subgiat in subgiats:
            for ls, s in zip(link_subs,subs):
                print(ls['link'], s['kode_sub_giat'])
            #   tampilkan list sub giat untuk masing-masing kegiatan giat 
            #   pilih subkegiatan yang akan diedit
                idp.choose_sub_giat(driver,s,ls["link"])
                akuns=findRekeningAkun(conn, s['kode_skpd'], s['kode_sub_skpd'], s['kode_bidang_urusan'], s['kode_program'], s['kode_giat'], s['kode_sub_giat'])
                akun_links=idp.list_akun(driver,s,False)
                count=0
                length=len(akuns)
                for ak,al in zip(akuns,akun_links):
                    if ak['kode_akun']==al['idRekSubRincObj']:
                         driver.switch_to.frame(driver.find_element_by_name("content"))
                         driver.implicitly_wait(1)
                         driver.find_element_by_xpath('//a[@href="'+al['link']+'"]').click()
                         driver.implicitly_wait(1)
                         driver.find_element_by_id('tb-edit').click()
                         driver.switch_to.default_content()
                         driver.switch_to.frame(driver.find_element_by_name("content"))
                         driver.implicitly_wait(0.5)

                         volume=driver.find_element_by_id('volume_rinc_0')
                         volume.clear()
                         satuan=driver.find_element_by_id('satuan_rinc_0')
                         satuan.clear()
                         harga=driver.find_element_by_id('harga_rinc_0')
                         harga.clear()

                         volume.send_keys('1')
                         satuan.send_keys('paket')
                         harga.send_keys(str(ak['total_rincian']))

                         driver.implicitly_wait(1)
                        
                         driver.find_element_by_id('tb-simpan').click()
                         driver.switch_to.default_content()
                         driver.switch_to.frame(driver.find_element_by_name("content"))
                         driver.implicitly_wait(0.5)

                         driver.find_element_by_id('tb-balik').click()
                         driver.switch_to.default_content()
                         count+=1
                         if(count==length):
                             driver.switch_to.frame(driver.find_element_by_name("content"))
                             driver.implicitly_wait(0.5)

                             driver.find_element_by_id('tb-balik').click()

            #   for akun in subgiat:
            #       tampilkan kode akun belanja untuk setiap subgiat
            #       ambil data dari sipd (backup) bandingkan dengan data yg ditampilkan di simral
            #       jika total_rincian sama:
            #           edit rincian yang ditampilkan di simral, harus sama dengan nilai di sipd
            #           simpan, kembali ke daftar akun, dst
            #       jika jumlah akun di sipd<akun di simral:
            #           edit rincian akun yang berbeda di simral isi dengan 0
            #           simpan, kembali ke daftar akun, dst
            #       jika jumlah akun di sipd>akun di simral:
            #           tambah rincian akun di simral yang berisi data kode, nama, dan total rincian akun yang ada di sipd
            #           simpan, kembali ke daftar akun, dst
driver.quit() 
conn.close()