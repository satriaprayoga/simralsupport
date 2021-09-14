from PyInquirer.prompt import prompt
from simral.driver.BkuPendapatanDriver import BkuPendapatanDriver
from simral.config.Config import Config
import csv

def file_pendapatan_prompt():
    file_propmpt={
        'type': 'input',
        'name': 'file',
        'message': 'File Pendapatan',
        'default': 'pendapatan_ppkd.csv',
    }
    answer=prompt(file_propmpt)
    return answer['file']

def input_bku_pendapatan(filename):
    config=Config()
    driver=BkuPendapatanDriver()
    driver.connect(r'./chromedriver.exe',False)
    driver.get_captcha()
    kasda_config=config.get_simral_pendapatan_config()
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
        driver.select_modul("Pendapatan", "objTreeMenu_1_node_1_2")
        driver.pilih_skpd()
        driver.input_bku_pendatan(d)
    f.close()
    driver.quit_driver()