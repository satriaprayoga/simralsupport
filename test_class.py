from simral.driver import DppaSimralDriver as dppa
from simral.config import Config as cfg

import logging

logging.basicConfig(level=logging.INFO)
config=cfg.Config()
sd=dppa.DppaSimralDriver('5.02.0.00.0.00.01.0000','BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH')
sd.connect(r'./chromedriver.exe',False)
sd.get_captcha()
print("Masukkan kode capcay:")
captcha=input()
anggaran_config=config.get_simral_perubahan_config()

sd.login(anggaran_config['username'],anggaran_config['password'],anggaran_config['cfg'],captcha)
sd.select_modul("Perubahan","objTreeMenu_1_node_2_2")

sd.import_pilih_kegiatan(anggaran_config['periode'],'5.02.0.00.0.00.01.0004','Bidang Akutansi dan Teknologi Informasi')
sd.import_kegiatan(anggaran_config['jenis_perubahan'])
