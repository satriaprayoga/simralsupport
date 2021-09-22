from simral.driver.ReportDriver import ReportDriver
from simral.config.Config import Config
import sqlite3

conn = sqlite3.connect("sipd_backup.db")

lra=ReportDriver()
lra.connect(r'./chromedriver.exe')
config=Config()
anggaran_config=config.get_simral_kasda_config()

print("masukkan captcha:")
capctha=input()

lra.login(anggaran_config['username'],anggaran_config['password'],anggaran_config['cfg'],int(capctha))
lra.select_modul("Kas Daerah", "objTreeMenu_1_node_6_5_1")
skpd={"kode_skpd":"5.02.0.00.0.00.01.0000","nama_skpd":"BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH"}
lra.download_report(skpd=skpd,subunit='SEMUA SUB UNIT',jenisLaporan='Realisasi Anggaran Satker Per Rek Jenis',tgl_mulai='1',bulan_mulai='Juli', tgl_selesai='22', bulan_selesai='September')