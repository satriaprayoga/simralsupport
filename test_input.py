from simral.driver.DppaSimralDriver import DppaSimralDriver
from simral.config.Config import Config
from simral.sipd.Backup import findKegiatan, findKegiatanByProgram, findProgramFromIdSkpd, findSkpdById, findSubkegiatan, findRekeningAkun

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
conn=sqlite3.connect("sipd_backup.db")
config=Config()
skpd=findSkpdById(conn,96)
driver=DppaSimralDriver(f'{skpd["kode_skpd"]}',f'{skpd["nama_skpd"]}')
driver.connect(r'./chromedriver.exe',False)
driver.get_captcha()
print("Masukkan kode capcay:")
captcha=input()
anggaran_config=config.get_simral_perubahan_config()
driver.login(anggaran_config['username'],anggaran_config['password'],anggaran_config['cfg'],captcha)
driver.select_modul("Perubahan","objTreeMenu_1_node_2_4_3")
program_fields=findProgramFromIdSkpd(conn,skpd['id_skpd'])
for field in program_fields:
    link_kegiatans=driver.input_list_kegiatan(anggaran_config['periode'],\
        f'[{field["kode_sub_skpd"]}] {field["nama_sub_skpd"]}',\
        f'[{field["kode_bidang_urusan"]}] {field["nama_bidang_urusan"]}',\
        f'[{field["kode_program"]}] {field["nama_program"]}')
    kegiatans=findKegiatan(conn,field["kode_skpd"],field["kode_sub_skpd"],\
                field["kode_bidang_urusan"], field["kode_program"])
    if(link_kegiatans!=None):
        for l,k in zip(link_kegiatans,kegiatans):
            if l['idKgtn']==k['kode_giat']:
                print("link: {}".format(l["link"]))
                driver.input_pilih_kegiatan(k,l['link'])
                sub_kegiatans=findSubkegiatan(conn,k["kode_skpd"],k["kode_sub_skpd"],\
                    k["kode_bidang_urusan"], k["kode_program"],k["kode_giat"])
                link_subs=driver.input_list_sub_kegiatan(k)
                sub_count=0
                len_sub=len(sub_kegiatans)
                for ls,sk in zip(link_subs,sub_kegiatans):
                    driver.input_pilih_sub_kegiatan(sk,ls['link'])
                    link_rincians=driver.input_list_rincian(sk)
                    akuns=findRekeningAkun(conn, sk['kode_skpd'], sk['kode_sub_skpd'], sk['kode_bidang_urusan'], sk['kode_program'], sk['kode_giat'], sk['kode_sub_giat'])
                    count=0
                    length=len(akuns)
                    for ak,lr in zip(akuns,link_rincians):
                        driver.input_edit_rincian(ak,lr)
                        count+=1
                        if count==length:
                            driver.back()
                    sub_count+=1
                if sub_count==len_sub:
                     driver.back()
            driver.refresh()
conn.close()
#driver.quit_driver()

