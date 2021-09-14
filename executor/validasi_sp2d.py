from PyInquirer.prompt import prompt
from simral.driver.ValidasiDriver import ValidasiDriver
from simral.config.Config import Config
import csv

def file_prompt():
    file_propmpt={
        'type': 'input',
        'name': 'file',
        'message': 'File Validasi',
        'default': 'validasi.csv',
    }
    answer=prompt(file_propmpt)
    return answer['file']

def validasi_sp2d_operation(filename):
    config=Config()
    driver=ValidasiDriver()
    driver.connect(r'./chromedriver.exe',False)
    driver.get_captcha()
    kasda_config=config.get_simral_kasda_config()
    captcha_prompt={
    'type': 'input',
    'name': 'captcha',
    'message': 'Masukkan kode captcha?',
    'filter': lambda val: int(val)
    }
    answer=prompt(captcha_prompt)
    driver.login(kasda_config['username'],kasda_config['password'],kasda_config['cfg'],answer['captcha'])
    f=open(filename,"r")
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

    driver.quit_driver()