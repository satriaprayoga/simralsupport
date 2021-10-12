from PyInquirer.prompt import prompt
from simral.driver.NeracaAwalDriver import NeracaAwalDriver
from simral.config.Config import Config

def file_neraca_prompt():
    file_propmpt={
        'type': 'input',
        'name': 'file',
        'message': 'File Neraca Awal',
        'default': 'NERACA_AWAL2021.xlsx',
    }
    answer=prompt(file_propmpt)
    return answer['file']

def neraca_awal_operation(filename):
    config=Config()
    driver=NeracaAwalDriver()
    data=driver.load_neraca_awal(filename)
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
    for index,row in data.iterrows():
        driver.select_modul("Akuntansi", "objTreeMenu_1_node_1_1")
        driver.pilih_skpd(row['Kode '],row['Satuan Kerja'],row['Sub Unit'])
        driver.input_neraca_awal(row['rekening_kelompok'],row['nama_kelompok'],row['rekening_jenis'],row['nama_jenis'],row['rekening_objek'],row['nama_objek'],row['Rekening_rincobjek'],row['nama_rincobjek'],row['Rekening'],row['Uraian'],row['Jumlah Debet'],row['Jumlah Kredit'])