from simral.driver.ValidasiDriver import ValidasiDriver
from simral.config.Config import Config

import logging
import csv

logging.basicConfig(level=logging.INFO)
config=Config()
driver=ValidasiDriver()
driver.connect(r'./chromedriver.exe',False)
driver.get_captcha()
print("Masukkan kode capcay:")
captcha=input()
kasda_config=config.get_simral_kasda_config()

driver.login(kasda_config['username'],kasda_config['password'],kasda_config['cfg'],captcha)

f=open("validasi.csv","r")
data_sp2d=csv.DictReader(f)
for d in data_sp2d:
    driver.select_modul("Kas Daerah", "objTreeMenu_1_node_2_4")
    data=driver.find_sp2d(d['no_sp2d'])
    driver.validasi_sp2d(data=data,refTable=d,tanggal_cair=d['tgl_cair'])
f.close()
invalid=driver.invalid

with open("invalid.csv","w") as inv:
    invalid_data=[]
    for i in invalid:
        invalid_data.append({"no_sp2d":i['noSp2d'],"jumlah":i["jumlah"],"keterangan":i["keterangan"]})
    csvwiter=csv.DictWriter(inv,['no_sp2d','jumlah','keterangan'])
    csvwiter.writeheader()
    csvwiter.writerows(invalid_data)


# driver = webdriver.Chrome(r'./chromedriver.exe')
# #driver.maximize_window()
# driver.set_window_size(1250,700)
# simral_login.connect_to_simral(driver)
# simral_login.find_captcha(driver)

# print("Masukkan kode captcha")
# captcha=input()

# if not captcha.isdigit():
#     logging.error("Format CAPTCHA salah!")
#     driver.quit()
#     exit(-1)

# simral_login.login(driver, USERNAME, PASSWORD, CFG, captcha)
# with open("validasi.csv","r") as f:
#     pendapatanCsv=csv.DictReader(f)
#     for d in pendapatanCsv:
#        val.modul_kasda(driver)
#        data=val.find_spd2d(driver, d['no_sp2d'], d['jumlah'])
#        if data:
#             if data['status']=='Proses Bank':
#                 if(data['jumlah']==int(d['jumlah'])):
#                     val.validasi_sp2d(driver,data,d['tgl_cair'])
#        else:
#             pass
# driver.implicitly_wait(2)
# driver.quit()


